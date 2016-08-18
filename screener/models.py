from django.db import models


class Question(models.Model):
    question = models.CharField(max_length=255)
    reference_answer = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', related_name='questions',
                             on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category', blank=True)

    def __str__(self):
        return self.question
    
    class Meta:
        unique_together = ("user", "question")
        ordering = ["-created"]
        

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name="answers")
    answer = models.TextField(blank=True)
    answer_correct = models.BooleanField()
    answer_quality = models.ForeignKey('AnswerQuality',
                             on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='answers',
                             on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE, 
                                  related_name='answers',
                                  null=True)
    def __str__(self):
        return self.answer
    
    class Meta:
        unique_together = ("question", "candidate")
        ordering = ["-created"]
    
    
class AnswerQuality(models.Model):
    quality = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.quality
        

class Category(models.Model):
    category = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey('auth.User', related_name='categories',
                             on_delete=models.CASCADE,
                             null=True)
    
    def __str__(self):
        return self.category
    
    class Meta:
        unique_together = ("category", "user")
        ordering = ["category"]
        verbose_name_plural = "categories"

        
class Screen(models.Model):
    name = models.CharField(max_length=50, 
                            verbose_name="Position title")
    user = models.ForeignKey('auth.User', related_name='screens',
                             on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name", "user")
        ordering = ["name"]
        
        
class Candidate(models.Model):
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    tel = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    about = models.TextField(blank=True)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, 
                               related_name='candidates')
    user = models.ForeignKey('auth.User', related_name='candidates',
                             on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.first_name + " " + self.surname
    
    class Meta:
        unique_together = ("first_name", "surname", "screen")
        ordering = ["screen"]
        


    
    
    