from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
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

from screener.views import (QuestionViewSet,
                            CategoryViewSet,
                            ScreenViewSet,
                            CandidateViewSet,
                            AnswerViewSet,
                            AnswerQualityViewSet)


DUMMY_VALUE = 'screener'

class QuestionViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username=DUMMY_VALUE, password=DUMMY_VALUE)
        self.user_imposter = User.objects.create_user(
            username="IMPOSTER", password=DUMMY_VALUE)
        self.factory = APIRequestFactory()
        self.client.login(username=self.user.username, password=DUMMY_VALUE)
        
    def create_question(self):
        self.question = Question.objects.create(question=DUMMY_VALUE, user=self.user)    
        
    def test_list(self):
        self.create_question()
        view = QuestionViewSet.as_view(actions={"get":"list"})
        request = self.factory.get(reverse('question-list'))
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        questions = response.data
        self.assertEqual(len(questions), 1)
        question = questions[0]
        self.assertEqual(question['question'], DUMMY_VALUE)
        self.assertEqual(question['pk'], 1)
        self.assertEqual(question['user'], DUMMY_VALUE)           
        
    def test_list_no_auth(self):
        self.create_question()
        view = QuestionViewSet.as_view(actions={"get":"list"})
        request = self.factory.get(reverse('question-list'))
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_list_different_users_questions(self):
        self.create_question()
        view = QuestionViewSet.as_view(actions={"get":"list"})
        request = self.factory.get(reverse('question-list'))
        force_authenticate(request, user=self.user_imposter)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        questions = response.data
        self.assertEqual(len(questions), 0)
        
    def test_detail_different_user(self):
        self.create_question()
        self.client.logout()
        self.client.login(username=self.user_imposter.username, password=DUMMY_VALUE)
        response = self.client.get(reverse('question-detail', 
                                           kwargs={'pk':self.question.pk}), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)        
    
    def test_put_different_user(self):
        self.create_question()
        self.client.logout()
        self.client.login(username=self.user_imposter.username, password=DUMMY_VALUE)
        response = self.client.put(reverse('question-detail', 
                                           kwargs={'pk':self.question.pk}),
                                   {'question': 'hack'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_different_user(self):
        self.create_question()
        self.client.logout()
        self.client.login(username=self.user_imposter.username, password=DUMMY_VALUE)
        response = self.client.delete(reverse('question-detail', 
                                              kwargs={'pk':self.question.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_post(self):
        response = self.client.post(reverse('question-list'),
                                   {'question': 'POST'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['question'], "POST")
    
    def test_put(self):
        self.create_question()
        response = self.client.put(reverse('question-detail', 
                                           kwargs={'pk':self.question.pk}),
                                   {'question': 'PUT'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['question'], "PUT")
    
    def test_delete(self):
        self.create_question()
        response = self.client.delete(reverse('question-detail', 
                                              kwargs={'pk':self.question.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        
class CategoryViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username=DUMMY_VALUE, password=DUMMY_VALUE)
        self.user_imposter = User.objects.create_user(
            username="IMPOSTER", password=DUMMY_VALUE)
        self.factory = APIRequestFactory()
        self.client.login(username=self.user.username, password=DUMMY_VALUE)
        
    def create_category(self):
        self.category = Category.objects.create(category=DUMMY_VALUE, user=self.user)    
        
    def test_list(self):
        self.create_category()
        view = CategoryViewSet.as_view(actions={"get":"list"})
        request = self.factory.get(reverse('category-list'))
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        categories = response.data
        self.assertEqual(len(categories), 17)        
        
    def test_list_no_auth(self):
        self.create_category()
        view = CategoryViewSet.as_view(actions={"get":"list"})
        request = self.factory.get(reverse('category-list'))
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_list_different_users_categories(self):
        self.create_category()
        view = CategoryViewSet.as_view(actions={"get":"list"})
        request = self.factory.get(reverse('category-list'))
        force_authenticate(request, user=self.user_imposter)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        categories = response.data
        self.assertEqual(len(categories), 16)
        
    def test_detail_different_user(self):
        self.create_category()
        self.client.logout()
        self.client.login(username=self.user_imposter.username, password=DUMMY_VALUE)
        response = self.client.get(reverse('category-detail', 
                                           kwargs={'pk':self.category.pk}), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)        
    
    def test_put_different_user(self):
        self.create_category()
        self.client.logout()
        self.client.login(username=self.user_imposter.username, password=DUMMY_VALUE)
        response = self.client.put(reverse('category-detail', 
                                           kwargs={'pk':self.category.pk}),
                                   {'category': 'hack'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_different_user(self):
        self.create_category()
        self.client.logout()
        self.client.login(username=self.user_imposter.username, password=DUMMY_VALUE)
        response = self.client.delete(reverse('category-detail', 
                                              kwargs={'pk':self.category.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_post(self):
        response = self.client.post(reverse('category-list'),
                                   {'category': 'POST'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['category'], "POST")
    
    def test_put(self):
        self.create_category()
        response = self.client.put(reverse('category-detail', 
                                           kwargs={'pk':self.category.pk}),
                                   {'category': 'PUT'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['category'], "PUT")
    
    def test_delete(self):
        self.create_category()
        response = self.client.delete(reverse('category-detail', 
                                              kwargs={'pk':self.category.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        
class ScreenViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username=DUMMY_VALUE, password=DUMMY_VALUE)
        self.user_imposter = User.objects.create_user(
            username="IMPOSTER", password=DUMMY_VALUE)
        self.factory = APIRequestFactory()
        self.client.login(username=self.user.username, password=DUMMY_VALUE)
        
    def create_screen(self):
        self.screen = Screen.objects.create(name=DUMMY_VALUE, user=self.user)    
        
    def test_list(self):
        self.create_screen()
        view = ScreenViewSet.as_view(actions={"get":"list"})
        request = self.factory.get(reverse('screen-list'))
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        screens = response.data
        self.assertEqual(len(screens), 1)
        screen = screens[0]
        self.assertEqual(screen['name'], DUMMY_VALUE)
        self.assertEqual(screen['pk'], 1)
        self.assertEqual(screen['user'], DUMMY_VALUE)           
        
    def test_list_no_auth(self):
        self.create_screen()
        view = ScreenViewSet.as_view(actions={"get":"list"})
        request = self.factory.get(reverse('screen-list'))
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_list_different_users_categories(self):
        self.create_screen()
        view = ScreenViewSet.as_view(actions={"get":"list"})
        request = self.factory.get(reverse('screen-list'))
        force_authenticate(request, user=self.user_imposter)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        screens = response.data
        self.assertEqual(len(screens), 0)
        
    def test_detail_different_user(self):
        self.create_screen()
        self.client.logout()
        self.client.login(username=self.user_imposter.username, password=DUMMY_VALUE)
        response = self.client.get(reverse('screen-detail', 
                                           kwargs={'pk':self.screen.pk}), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)        
    
    def test_put_different_user(self):
        self.create_screen()
        self.client.logout()
        self.client.login(username=self.user_imposter.username, password=DUMMY_VALUE)
        response = self.client.put(reverse('screen-detail', 
                                           kwargs={'pk':self.screen.pk}),
                                   {'name': 'hack'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_different_user(self):
        self.create_screen()
        self.client.logout()
        self.client.login(username=self.user_imposter.username, password=DUMMY_VALUE)
        response = self.client.delete(reverse('screen-detail', 
                                              kwargs={'pk':self.screen.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_post(self):
        response = self.client.post(reverse('screen-list'),
                                   {'name': 'POST'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "POST")
    
    def test_put(self):
        self.create_screen()
        response = self.client.put(reverse('screen-detail', 
                                           kwargs={'pk':self.screen.pk}),
                                   {'name': 'PUT'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "PUT")
    
    def test_delete(self):
        self.create_screen()
        response = self.client.delete(reverse('screen-detail', 
                                              kwargs={'pk':self.screen.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        

class AnswerViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username=DUMMY_VALUE, password=DUMMY_VALUE)
        self.user_imposter = User.objects.create_user(
            username="IMPOSTER", password=DUMMY_VALUE)
        self.factory = APIRequestFactory()
        self.client.login(username=self.user.username, password=DUMMY_VALUE)
        self.screen = Screen.objects.create(name=DUMMY_VALUE, user=self.user)
        self.answer_quality = AnswerQuality.objects.create(quality=DUMMY_VALUE)
        data = {'first_name': DUMMY_VALUE,
                'surname': DUMMY_VALUE,
                'tel': DUMMY_VALUE,
                'email': 'screener@screener.com',
                'screen': self.screen}
        self.candidate = Candidate.objects.create(user=self.user, **data)
        self.question = Question.objects.create(question=DUMMY_VALUE, user=self.user)

        
    def create_answer(self):
        data = {'question': self.question,
                'answer': DUMMY_VALUE,
                'answer_correct': True,
                'answer_quality': self.answer_quality,
                'candidate': self.candidate,
                'user':self.user}
        self.answer = Answer.objects.create(**data)    
        
    def test_list(self):
        self.create_answer()
        view = AnswerViewSet.as_view(actions={"get":"list"})
        request = self.factory.get(reverse('answer-list'))
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        answers = response.data
        self.assertEqual(len(answers), 1)
        answer = answers[0]
        self.assertEqual(answer['answer'], DUMMY_VALUE)
        self.assertEqual(answer['pk'], 1)
        self.assertEqual(answer['user'], DUMMY_VALUE)           
        
    def test_list_no_auth(self):
        self.create_answer()
        view = AnswerViewSet.as_view(actions={"get":"list"})
        request = self.factory.get(reverse('answer-list'))
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_list_different_users_answers(self):
        self.create_answer()
        view = AnswerViewSet.as_view(actions={"get":"list"})
        request = self.factory.get(reverse('answer-list'))
        force_authenticate(request, user=self.user_imposter)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        answers = response.data
        self.assertEqual(len(answers), 0)
        
    def test_detail_different_user(self):
        self.create_answer()
        self.client.logout()
        self.client.login(username=self.user_imposter.username, password=DUMMY_VALUE)
        response = self.client.get(reverse('answer-detail', 
                                           kwargs={'pk':self.answer.pk}), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)        
    
    def test_put_different_user(self):
        self.create_answer()
        self.client.logout()
        self.client.login(username=self.user_imposter.username, password=DUMMY_VALUE)
        data = {'question': self.question.pk,
                'answer': 'PUT',
                'answer_correct': True,
                'answer_quality': self.answer_quality.pk,
                'candidate': self.candidate.pk}
        response = self.client.put(reverse('answer-detail', 
                                           kwargs={'pk':self.answer.pk}),
                                   data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_different_user(self):
        self.create_answer()
        self.client.logout()
        self.client.login(username=self.user_imposter.username, password=DUMMY_VALUE)
        response = self.client.delete(reverse('answer-detail', 
                                              kwargs={'pk':self.answer.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_post(self):
        data = {'question': self.question.pk,
                'answer': 'POST',
                'answer_correct': True,
                'answer_quality': self.answer_quality.pk,
                'candidate': self.candidate.pk}
        response = self.client.post(reverse('answer-list'),
                                    data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['answer'], "POST")
    
    def test_put(self):
        self.create_answer()
        data = {'question': self.question.pk,
                'answer': 'PUT',
                'answer_correct': True,
                'answer_quality': self.answer_quality.pk,
                'candidate': self.candidate.pk}
        response = self.client.put(reverse('answer-detail', 
                                           kwargs={'pk':self.answer.pk}),
                                   data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['answer'], "PUT")
    
    def test_delete(self):
        self.create_answer()
        response = self.client.delete(reverse('answer-detail', 
                                              kwargs={'pk':self.answer.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        
class AnswerQualityViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username=DUMMY_VALUE, password=DUMMY_VALUE)
        self.user_imposter = User.objects.create_user(
            username="IMPOSTER", password=DUMMY_VALUE)
        self.factory = APIRequestFactory()
        self.client.login(username=self.user.username, password=DUMMY_VALUE)
        self.answer_quality = AnswerQuality.objects.create(quality=DUMMY_VALUE)  
        
    def test_list(self):
        view = AnswerQualityViewSet.as_view(actions={"get":"list"})
        request = self.factory.get(reverse('answerquality-list'))
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        answers_qualities = response.data
        self.assertEqual(len(answers_qualities), 4)    
        
    def test_list_no_auth(self):
        view = AnswerQualityViewSet.as_view(actions={"get":"list"})
        request = self.factory.get(reverse('answerquality-list'))
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete(self):
        response = self.client.delete(reverse('answerquality-detail', 
                                              kwargs={'pk':self.answer_quality.pk}))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_post(self):
        data = {'quality': DUMMY_VALUE}
        response = self.client.post(reverse('answerquality-list'),
                                    data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_put(self):
        data = {'quality': DUMMY_VALUE}
        response = self.client.put(reverse('answerquality-detail', 
                                           kwargs={'pk':self.answer_quality.pk}),
                                   data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class CandidateViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username=DUMMY_VALUE, password=DUMMY_VALUE)
        self.user_imposter = User.objects.create_user(
            username="IMPOSTER", password=DUMMY_VALUE)
        self.factory = APIRequestFactory()
        self.client.login(username=self.user.username, password=DUMMY_VALUE)
        self.screen = Screen.objects.create(name=DUMMY_VALUE, user=self.user)
        self.url_screen = reverse('screen-detail', kwargs={'pk':self.screen.pk}) 
        data = {'first_name': DUMMY_VALUE,
                'surname': DUMMY_VALUE,
                'tel': DUMMY_VALUE,
                'email': 'screener@screener.com',
                'screen':self.screen
                }
        self.candidate = Candidate.objects.create(user=self.user, **data)
           
        
    def test_list(self):
        view = CandidateViewSet.as_view(actions={"get":"list"})
        request = self.factory.get(reverse('candidate-list'))
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        candidates = response.data
        self.assertEqual(len(candidates), 1)
        candidate = candidates[0]
        self.assertEqual(candidate['first_name'], DUMMY_VALUE)
        self.assertEqual(candidate['surname'], DUMMY_VALUE)
        self.assertEqual(candidate['pk'], 1)
        self.assertEqual(candidate['user'], DUMMY_VALUE)           
    
    
    def test_list_no_auth(self):
        view = CandidateViewSet.as_view(actions={"get":"list"})
        request = self.factory.get(reverse('candidate-list'))
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_list_different_users_candidates(self):
        view = CandidateViewSet.as_view(actions={"get":"list"})
        request = self.factory.get(reverse('candidate-list'))
        force_authenticate(request, user=self.user_imposter)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        candidates = response.data
        self.assertEqual(len(candidates), 0)
        
    def test_detail(self):
        response = self.client.get(reverse('candidate-detail', 
                                           kwargs={'pk':self.candidate.pk}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], DUMMY_VALUE)
        
    def test_detail_different_user(self):
        self.client.logout()
        self.client.login(username=self.user_imposter.username, password=DUMMY_VALUE)
        response = self.client.get(reverse('candidate-detail', 
                                           kwargs={'pk':self.candidate.pk}), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)        
    
    def test_put_different_user(self):
        self.client.logout()
        self.client.login(username=self.user_imposter.username, password=DUMMY_VALUE)
        data = {'first_name': DUMMY_VALUE,
                'surname': DUMMY_VALUE,
                'tel': DUMMY_VALUE,
                'email': 'screener@screener.com',
                'screen':self.url_screen
                }
        response = self.client.put(reverse('candidate-detail', 
                                           kwargs={'pk':self.candidate.pk}),
                                   data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_different_user(self):
        self.client.logout()
        self.client.login(username=self.user_imposter.username, password=DUMMY_VALUE)
        response = self.client.delete(reverse('candidate-detail', 
                                              kwargs={'pk':self.candidate.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_post(self):
        data = {'first_name': 'POST',
                'surname': DUMMY_VALUE,
                'tel': DUMMY_VALUE,
                'email': 'screener@screener.com',
                'screen':self.url_screen
                }
        response = self.client.post(reverse('candidate-list'),
                                    data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], "POST")
    
    def test_put(self):
        data = {'first_name': 'PUT',
                'surname': DUMMY_VALUE,
                'tel': DUMMY_VALUE,
                'email': 'screener@screener.com',
                'screen':self.url_screen
                }
        response = self.client.put(reverse('candidate-detail', 
                                           kwargs={'pk':self.candidate.pk}),
                                   data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "PUT")
    
    def test_delete(self):
        response = self.client.delete(reverse('candidate-detail', 
                                              kwargs={'pk':self.candidate.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
        