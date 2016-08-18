from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'questions', views.QuestionViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'screens', views.ScreenViewSet)
router.register(r'candidates', views.CandidateViewSet)
router.register(r'answers', views.AnswerViewSet)
router.register(r'answerquality', views.AnswerQualityViewSet)

urlpatterns = [
    url(r'^$', views.index,{'template_name': 'screener/index.html'}, name='index'),
    url(r'^api/', include(router.urls)),
    # comment in to browse the API if you do not have login functionality http://127.0.0.1:8000/screener/api/
    #url(r'^api-auth/', include('rest_framework.urls')),
]
