from django.urls import path, re_path
from . import views
from django.conf import settings
from django.views.static import serve
urlpatterns = [
    path('<slug:user>/questions/<slug:question>/', views.QuestionDetailView, name='question_detail'),
    path('questions/create', views.QuestionCreateView.as_view(), name='create_question'),
    path('answer/<slug:question>/', views.AnswerCreateView.as_view(),name='answer'),
    path('trending/questions/', views.TrendingQuestionView.as_view(), name='trending'),
    path('like/', views.likePost, name='like_question'),
	path('like/answer/', views.likeAnswer, name='like_answer')
]

if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^uploads/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    ]