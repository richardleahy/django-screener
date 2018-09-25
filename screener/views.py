from __future__ import division
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import (api_view, 
                                       permission_classes)
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework import pagination
from rest_framework.decorators import detail_route

from screener.serializers import (QuestionSerializer, 
                                  CategorySerializer,
                                  ScreenSerializer,
                                  CandidateSerializer,
                                  AnswerSerializer,
                                  AnswerQualitySerializer)

from screener.models import (Question,
                             Category,
                             Screen,
                             Candidate,
                             Answer,
                             AnswerQuality)
from screener.permissions import IsOwner


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'questions': reverse('question-list', request=request, format=format),
        'categories': reverse('category-list', request=request, format=format),
        'screens': reverse('screen-list', request=request, format=format),
        'candidates': reverse('candidate-list', request=request, format=format),
        'answers': reverse('answer-list', request=request, format=format),
        'answerquality': reverse('answerquality-list', request=request, format=format)
    })
    
    
class AllResultsSetPagination(pagination.BasePagination):
    """Return all paginated results."""
    def paginate_queryset(self, queryset, request, view=None):
        return queryset
    
    def get_paginated_response(self, data):
        return Response(data)
    
    
class QuestionViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = Question.objects.none()
    serializer_class = QuestionSerializer
    pagination_class = AllResultsSetPagination
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        return Question.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        
class CategoryViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = Category.objects.none()
    serializer_class = CategorySerializer
    pagination_class = AllResultsSetPagination
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        return Category.objects.filter(Q(user=None) | 
                                       Q(user=self.request.user))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

def calculate_score(candidate_pk, screen_pk, user):
    """Calculate the candidates score.

    Arguments:
    candidate_pk -- the candidate pk
    screen_pk -- the screen pk
    user -- the user object
    """
    screen = Screen.objects.get(pk=screen_pk, user=user)
    questions = list(screen.questions.values_list('pk', flat=True))
    questions_answered = Answer.objects.filter(candidate=candidate_pk,
                                               question__in=questions,
                                               user=user)
    
    correct_answers = \
        questions_answered.filter(answer_correct=True).count()
    try:
        score = round(correct_answers / len(questions) * 100, 2)
    except ZeroDivisionError:
        score = 0
    return score, questions_answered.count()


def calculate_quality_breakdown(candidate_pk, screen_pk, user):
    """Calculate the candidates quality breakdown.

    Arguments:
    candidate_pk -- the candidate pk
    screen_pk -- the screen pk
    user -- the user object
    """
    screen = Screen.objects.get(pk=screen_pk, user=user)
    questions = list(screen.questions.values_list('pk', flat=True))
    
    questions_answered = Answer.objects.filter(candidate=candidate_pk,
                                               question__in=questions,
                                               user=user)
    qualities = AnswerQuality.objects.all()
    breakdown = []
    for quality in qualities:
        quality_count = questions_answered.filter(
            answer_quality=quality).count()
        try:
            quality_percent = \
                round(quality_count / len(questions_answered) * 100, 2)
        except ZeroDivisionError:
            quality_percent = 'N/A'
        breakdown.append((quality.quality, quality_percent))
    return breakdown

        
class ScreenViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = Screen.objects.none()
    serializer_class = ScreenSerializer
    pagination_class = AllResultsSetPagination
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    
    @detail_route(methods=['get'], 
                  permission_classes=[permissions.IsAuthenticated, 
                                      IsOwner])
    def score(self, request, pk):
        """Calculate the candidates score.
    
        Arguments:
        request -- the request object
        pk -- the screen pk
        """
        candidate = self.request.query_params.get('candidate')
        try:
            Screen.objects.get(pk=pk, user=self.request.user)
        except Screen.DoesNotExist:
            return Response({"detail":"Not found", "status_code":404})
        
        score, questions_answered = calculate_score(candidate, pk, 
                                                    self.request.user)
        return Response({'score':score, 'questions_answered':questions_answered})
 
    def get_queryset(self):
        return Screen.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        
class CandidateViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = Candidate.objects.none()
    serializer_class = CandidateSerializer
    pagination_class = AllResultsSetPagination
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    
    def get_queryset(self):
        queryset = Candidate.objects.filter(user=self.request.user)
        screen = self.request.query_params.get('screen', None)
        if screen is not None:
            queryset = queryset.filter(screen=screen)
        for candidate in queryset:
            candidate.score, candidate.questions_answered = \
                calculate_score(candidate.pk, candidate.screen.pk, 
                                self.request.user)
            candidate.quality = \
                str(calculate_quality_breakdown(candidate.pk, 
                                                candidate.screen.pk, 
                                                self.request.user))

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

class AnswerViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = Answer.objects.none()
    serializer_class = AnswerSerializer
    pagination_class = AllResultsSetPagination
    permission_classes = (permissions.IsAuthenticated, IsOwner)
        
    def get_queryset(self):
        queryset = Answer.objects.filter(user=self.request.user)
        question = self.request.query_params.get('question', None)
        questions = self.request.query_params.get('questions', None)
        candidate = self.request.query_params.get('candidate', None)
        
        if questions is not None:
            queryset = queryset.filter(question__in=questions)
        if questions is None and question is not None:
            queryset = queryset.filter(question=question)
        if candidate is not None:
            queryset = queryset.filter(candidate=candidate)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        
class AnswerQualityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = AnswerQuality.objects.none()
    serializer_class = AnswerQualitySerializer
    pagination_class = AllResultsSetPagination
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        return AnswerQuality.objects.all()

        

