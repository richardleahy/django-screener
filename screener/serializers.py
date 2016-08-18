from rest_framework import serializers
from django.db.models import Q
from screener.models import (Question,
                             Category,
                             Screen,
                             Candidate,
                             Answer, AnswerQuality) 


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """Serialize the Category model."""
    
    class Meta:
        model = Category
        fields = ('pk', 'category', 'user', 'url')
        
    user = serializers.ReadOnlyField(source='user.username')
    
    def update(self, instance, validated_data):
        """Update category.
    
        Validate that the category does not already exist.
        """
        c = validated_data.get('category', instance.category).strip()
        if instance.category.lower() != c.lower():
            category_exists = \
                Category.objects.filter(user=self.context['request'].user,
                                        category__iexact=c)
            if category_exists:
                raise serializers.ValidationError(
                    {'detail': 'Category already exists.'}) 
            
        instance.category = c
        instance.save()
        return instance
    
    def create(self, validated_data):
        """Create new category.
    
        Validate that the category does not already exist.
        """
        category_exists = \
            Category.objects.filter(
                Q(user=self.context['request'].user) | Q(user=None),
                category__iexact=validated_data['category'].strip()
            )
        if category_exists:
            raise serializers.ValidationError(
                {'detail': 'Category already exists.'}) 
        
        category = Category.objects.create(**validated_data)
        return category


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    """Serialize the Question model."""
        
    class Meta:
        model = Question
        fields = ('pk', 'question', 'reference_answer', 'user', 
                  'url', "categories", "answers")

    categories = CategorySerializer(many=True, required=False)    
    user = serializers.ReadOnlyField(source='user.username')
    answers = serializers.HyperlinkedRelatedField(
        many=True,
        required=False,
        view_name='answer-detail',
        queryset = Answer.objects.all()
    )
    
    def update(self, instance, validated_data):
        """Update question.
    
        Validate that the question does not already exist.
        """
        q = validated_data.get('question', instance.question).strip()
        if instance.question.lower() != q.lower():
            question_exists = \
                Question.objects.filter(user=self.context['request'].user,
                                        question__iexact=q)
            if question_exists:
                raise serializers.ValidationError(
                    {'detail': 'Question already exists.'}) 
            
        instance.question = q
        instance.reference_answer = \
            validated_data.get('reference_answer', 
                               instance.reference_answer)
        instance.save()
        
        categories = validated_data.pop('categories', None)
        if categories or categories == []:
            instance.categories.clear()
            for category in categories:
                c = Category.objects.get(Q(user=self.context['request'].user) 
                                         | Q(user=None),
                                         **category)
                instance.categories.add(c)
        return instance
    
    def create(self, validated_data):
        """Create new question.
    
        Validate that the question does not already exist.
        """
        q = validated_data['question'].strip()
        question_exists = \
            Question.objects.filter(user=self.context['request'].user,
                                    question__iexact=q)
        if question_exists:
            raise serializers.ValidationError(
                {'detail': 'Question already exists.'}) 
        
        categories = validated_data.pop('categories', None)
        question = Question.objects.create(**validated_data)
        
        if categories:
            for category in categories:
                try:
                    # Check if user category already exists and use it.
                    c = Category.objects.get(Q(user=self.context['request'].user) 
                                             | Q(user=None),
                                             **category)
                except Category.DoesNotExist:
                    # Category does exist, create new one.
                    c = Category.objects.create(user=self.context['request'].user,
                                                **category)
                question.categories.add(c)
        return question
    
    
class ScreenSerializer(serializers.HyperlinkedModelSerializer):
    """Serialize the Screen model."""
    
    def __init__(self, *args, **kwargs):
        super(ScreenSerializer, self).__init__(*args, **kwargs)
        self.fields['candidates'].child_relation.queryset = \
            Candidate.objects.filter(user=self.context['request'].user)
            
    class Meta:
        model = Screen
        fields = ('pk', 'name', 'user', 'url', "questions", "candidates")

    questions = QuestionSerializer(many=True, required=False)
    
    user = serializers.ReadOnlyField(source='user.username')
    candidates = serializers.HyperlinkedRelatedField(
        many=True,
        required=False,
        view_name='candidate-detail',
        queryset = Candidate.objects.all()
    )
    
    def validate_name(self, name):
        """Validate the screen name.
    
        Arguments:
        name -- the screen name
        """
        if self.instance is not None:
            #update
            s = Screen.objects.get(pk=self.instance.pk)
            if s.name.strip().lower() == name.strip().lower():
                return name

        screen_exists = Screen.objects.filter(user=self.context['request'].user,
                                              name__iexact=name)
        if screen_exists:
            raise serializers.ValidationError({'name': '%s already exists.' % name}) 
        return name
    
    def create(self, validated_data):
        """Create new screen."""
        questions = validated_data.pop('questions', None)
        screen = Screen.objects.create(**validated_data)
        
        if questions:
            for question in questions:
                try:
                    # Check if user question already exists and use it.
                    q = Question.objects.get(user=self.context['request'].user,
                                             **question)
                except Question.DoesNotExist:
                    # Question does not exist, create new one.
                    q = Question.objects.create(user=self.context['request'].user,
                                                **question)
                screen.questions.add(q)
        return screen
    
    def update(self, instance, validated_data):
        """Update screen."""          
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        
        questions = validated_data.pop('questions', None)
        if questions or questions == []:
            instance.questions.clear()
            for question in questions:
                q = Question.objects.get(user=self.context['request'].user,
                                         **question)
                instance.questions.add(q)
        return instance
    
    
class CandidateSerializer(serializers.HyperlinkedModelSerializer):
    """Serialize the Candidate model."""
    
    def __init__(self, *args, **kwargs):
        super(CandidateSerializer, self).__init__(*args, **kwargs)
        self.fields['screen'].queryset = \
            Screen.objects.filter(user=self.context['request'].user)
    
    class Meta:
        model = Candidate
        fields = ('pk', 'first_name', 'user', 'url',
                  'surname', 'tel', 'email', 'screen','screen_name',
                  'screen_pk', 'user_pk', 'score', 'quality')

    screen_name = serializers.ReadOnlyField(source='screen.name')  
    screen_pk = serializers.ReadOnlyField(source='screen.pk')
    user = serializers.ReadOnlyField(source='user.username')
    user_pk = serializers.ReadOnlyField(source='user.pk')
    score = serializers.ReadOnlyField()
    quality = serializers.ReadOnlyField()
    
    
class AnswerSerializer(serializers.ModelSerializer):
    """Serialize the Answer model."""
    
    def __init__(self, *args, **kwargs):
        super(AnswerSerializer, self).__init__(*args, **kwargs)
        self.fields['question'].queryset = \
            Question.objects.filter(user=self.context['request'].user)  
        self.fields['candidate'].queryset = \
            Candidate.objects.filter(user=self.context['request'].user)       
        
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Answer
        fields = ('pk', 'answer', 'question', 'url',
                  'candidate', 'user', 'answer_correct', 
                  'answer_quality')
        
        
class AnswerQualitySerializer(serializers.HyperlinkedModelSerializer):
    """Serialize the AnswerQuality model."""
    
    class Meta:
        model = AnswerQuality
        fields = ('pk', 'quality', 'url')
        