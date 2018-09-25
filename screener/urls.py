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
    url(r'^', include(router.urls)),
    # Remove comment to login into the API if you do not have any login functionality
    #url(r'^api-auth/', include('rest_framework.urls')),
]
