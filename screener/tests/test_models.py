from rest_framework.test import APIRequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, AnonymousUser
from rest_framework import status
from rest_framework.test import APITestCase

from screener.models import (Question,
                             Category,
                             Screen,
                             Candidate,
                             Answer,
                             AnswerQuality)


class QuestionTests(APITestCase):
    NAME = 'screener'
    
    def setUp(self):
        self.user = User.objects.create_user(
            username=QuestionTests.NAME, password=QuestionTests.NAME)
        self.client.login(username=QuestionTests.NAME, password=QuestionTests.NAME)
        
    def test_create_question(self):
        """
        Ensure we can create a new question object.
        """
        Category.objects.create(category=QuestionTests.NAME)
        
        url = reverse('question-list')
        data = {'question': QuestionTests.NAME,
                'reference_answer':QuestionTests.NAME,
                'categories':[{'category':QuestionTests.NAME}]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Question.objects.get().question, QuestionTests.NAME)
        self.assertEqual(Question.objects.get().reference_answer, QuestionTests.NAME)
        self.assertEqual(len(Question.objects.get().categories.all()), 1)
        category = Question.objects.get().categories.all()[0]
        self.assertEqual(category.category, QuestionTests.NAME)
        
    def test_create_question_invalid_auth(self):
        """
        Ensure we can not create a new question object without authentication.
        """
        url = reverse('question-list')
        data = {'question': QuestionTests.NAME}
        self.client.logout()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Question.objects.count(), 0)
        
    def test_create_question_with_required_values_missing(self):
        """
        Ensure we can not create a new question object with required data missing.
        """
        url = reverse('question-list')
        data = {'reference_answer':QuestionTests.NAME}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Question.objects.count(), 0)
        
    def test_string_representation(self):
        """
        Test __str__ has been set on the model correctly.
        """
        question = Question(question=QuestionTests.NAME)
        self.assertEqual(str(question), QuestionTests.NAME)
        
        
class CategoryTests(APITestCase):
    NAME = 'screener'
    
    def setUp(self):
        self.user = User.objects.create_user(
            username=QuestionTests.NAME, password=QuestionTests.NAME)
        self.client.login(username=QuestionTests.NAME, password=QuestionTests.NAME)
        
    def test_create_category(self):
        """
        Ensure we can create a new category.
        """
        url = reverse('category-list')
        data = {'category': CategoryTests.NAME}
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 17)
        self.assertEqual(Category.objects.get(category=CategoryTests.NAME).category, CategoryTests.NAME)
        
    def test_create_category_invalid_auth(self):
        """
        Ensure we can not create a new category object without authentication.
        """
        url = reverse('category-list')
        data = {'category': CategoryTests.NAME}
        self.client.logout()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_create_category_with_required_values_missing(self):
        """
        Ensure we can not create a new category object with required data missing.
        """
        url = reverse('category-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_string_representation(self):
        """
        Test __str__ has been set on the model correctly.
        """
        category = Category(category=CategoryTests.NAME)
        self.assertEqual(str(category), CategoryTests.NAME)
        
        
class ScreenTests(APITestCase):
    NAME = 'screener'
    
    def setUp(self):
        self.user = User.objects.create_user(
            username=QuestionTests.NAME, password=QuestionTests.NAME)
        self.client.login(username=QuestionTests.NAME, password=QuestionTests.NAME)
        
    def test_create_screen(self):
        """
        Ensure we can create a new screen.
        """
        url = reverse('screen-list')
        data = {'name': ScreenTests.NAME,
                'questions':[{'question':ScreenTests.NAME}]}
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Screen.objects.count(), 1)
        self.assertEqual(Screen.objects.get().name, ScreenTests.NAME)
        
        self.assertEqual(len(Screen.objects.get().questions.all()), 1)
        question = Screen.objects.get().questions.all()[0]
        self.assertEqual(question.question, ScreenTests.NAME)
        
    def test_create_screen_invalid_auth(self):
        """
        Ensure we can not create a new screen object without authentication.
        """
        url = reverse('screen-list')
        data = {'name': ScreenTests.NAME}
        self.client.logout()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Screen.objects.count(), 0)
        
    def test_create_screen_with_required_values_missing(self):
        """
        Ensure we can not create a new screen object with required data missing.
        """
        url = reverse('screen-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Screen.objects.count(), 0)
        
    def test_string_representation(self):
        """
        Test __str__ has been set on the model correctly.
        """
        screen = Screen(name=ScreenTests.NAME)
        self.assertEqual(str(screen), ScreenTests.NAME)
        
        
class CandidateTests(APITestCase):
    NAME = 'screener'
    
    def setUp(self):
        self.user = User.objects.create_user(
            username=QuestionTests.NAME, password=QuestionTests.NAME)
        self.client.login(username=QuestionTests.NAME, password=QuestionTests.NAME)

    def test_create_candidate(self):
        """
        Ensure we can create a new candidate.
        """
        s = Screen.objects.create(name=CandidateTests.NAME, user=self.user)
        url = reverse('candidate-list')
        url_screen = reverse('screen-detail', kwargs={'pk':s.pk}) 
        data = {'first_name': CandidateTests.NAME,
                'surname': CandidateTests.NAME,
                'tel': CandidateTests.NAME,
                'email': 'screener@screener.com',
                'screen':url_screen
                }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Candidate.objects.count(), 1)
        self.assertEqual(Candidate.objects.get().first_name, CandidateTests.NAME)
        self.assertEqual(Candidate.objects.get().surname, CandidateTests.NAME)
        self.assertEqual(Candidate.objects.get().tel, CandidateTests.NAME)
        self.assertEqual(Candidate.objects.get().email, 'screener@screener.com')
        self.assertEqual(Candidate.objects.get().screen.name, CandidateTests.NAME)
        
    def test_create_candidate_invalid_auth(self):
        """
        Ensure we can not create a new candidate object without authentication.
        """
        s = Screen.objects.create(name=CandidateTests.NAME, user=self.user)
        url_screen = reverse('screen-detail', kwargs={'pk':s.pk}) 
        data = {'first_name': CandidateTests.NAME,
                'surname': CandidateTests.NAME,
                'tel': CandidateTests.NAME,
                'email': CandidateTests.NAME,
                'screen': url_screen}
        url = reverse('candidate-list')
        
        self.client.logout()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Candidate.objects.count(), 0)
        
    def test_create_candidate_with_required_values_missing(self):
        """
        Ensure we can not create a new candidate object with required data missing.
        """
        url = reverse('candidate-list')
        data = {'tel': CandidateTests.NAME,
                'email': CandidateTests.NAME,
                'about': CandidateTests.NAME}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Candidate.objects.count(), 0)
        
    def test_string_representation(self):
        """
        Test __str__ has been set on the model correctly.
        """
        candidate = Candidate(first_name=CandidateTests.NAME,
                              surname=CandidateTests.NAME)
        self.assertEqual(str(candidate), CandidateTests.NAME + ' ' +  CandidateTests.NAME)
        
        
class AnswerTests(APITestCase):
    NAME = 'screener'
    
    def setUp(self):
        self.user = User.objects.create_user(
            username=AnswerTests.NAME, password=AnswerTests.NAME)
        self.client.login(username=AnswerTests.NAME, password=AnswerTests.NAME)
        
        self.answer_quality = AnswerQuality.objects.create(quality=AnswerTests.NAME)
        self.url_quality = reverse('answerquality-detail', kwargs={'pk':self.answer_quality.pk})
        
        self.screen = Screen.objects.create(name=AnswerTests.NAME, user=self.user)
        self.url_screen = reverse('screen-detail', kwargs={'pk':self.screen.pk}) 
        
        data = {'first_name': AnswerTests.NAME,
                'surname': AnswerTests.NAME,
                'tel': AnswerTests.NAME,
                'email': AnswerTests.NAME,
                'screen': self.screen}
        self.candidate = Candidate.objects.create(user=self.user, **data)
        self.url_candidate = reverse('candidate-detail', kwargs={'pk':self.candidate.pk})
        
        self.question = Question.objects.create(question=AnswerTests.NAME, user=self.user)
        self.url_question = reverse('question-detail', kwargs={'pk':self.question.pk})


    def test_create_answer(self):
        """
        Ensure we can create a new answer.
        """
        url = reverse('answer-list')
        data = {'question': self.question.pk,
                'answer': AnswerTests.NAME,
                'answer_correct': True,
                'answer_quality': self.answer_quality.pk,
                'candidate': self.candidate.pk}
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Answer.objects.count(), 1)
        self.assertEqual(Answer.objects.get().answer, CategoryTests.NAME)
        self.assertEqual(Answer.objects.get().answer_correct, True)
        self.assertEqual(Answer.objects.get().answer_quality.quality, self.answer_quality.quality)
        self.assertEqual(Answer.objects.get().candidate.first_name, self.candidate.first_name)
        self.assertEqual(Answer.objects.get().question.question, self.question.question)
    
    
    def test_create_answer_invalid_auth(self):
        """
        Ensure we can not create a new answer object without authentication.
        """
        url = reverse('answer-list')
        data = {'question': self.question.pk,
                'answer': AnswerTests.NAME,
                'answer_correct': True,
                'answer_quality': self.answer_quality.pk,
                'candidate': self.candidate.pk}
        self.client.logout()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Answer.objects.count(), 0)
        
    def test_create_answer_with_required_values_missing(self):
        """
        Ensure we can not create a new answer object with required data missing.
        """
        url = reverse('answer-list')
        data = {'question': self.question.pk,
                'answer_correct': True,
                'candidate': self.candidate.pk}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Answer.objects.count(), 0)
        
    def test_string_representation(self):
        """
        Test __str__ has been set on the model correctly.
        """
        answer = Answer(answer=AnswerTests.NAME)
        self.assertEqual(str(answer), AnswerTests.NAME)
        
        
class AnswerQualityTests(APITestCase):
    NAME = 'screener'
    
    def setUp(self):
        self.user = User.objects.create_user(
            username=AnswerTests.NAME, password=AnswerTests.NAME)
        self.client.login(username=AnswerTests.NAME, password=AnswerTests.NAME)

    def test_cannot_create_answer_quality(self):
        """
        Ensure we can not create a new answer quality. POST ONLY.
        """
        url = reverse('answerquality-list')
        data = {'quality': AnswerQualityTests.NAME}
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
    def test_list_invalid_auth(self):
        """
        Ensure we can not retrieve objects without authentication.
        """
        url = reverse('answerquality-list')
        self.client.logout()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_string_representation(self):
        """
        Test __str__ has been set on the model correctly.
        """
        answerquality = AnswerQuality(quality=AnswerQualityTests.NAME)
        self.assertEqual(str(answerquality), AnswerQualityTests.NAME)
      
        
        