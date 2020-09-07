from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserProfileSerializer, ProgrammingLanguageSerializer, QuestionSerializer
from accounts.models import UserProfile, ProgrammingLanguage
from questions.models import Question
from django.conf import settings
import json
from django.http import JsonResponse
from django.conf import settings
from django.urls import URLPattern, URLResolver

class UserProfileListView(APIView):
	def get(self, request):
		qs = UserProfile.objects.all().order_by('-points')
		serializer = UserProfileSerializer(qs, many=True)
		return Response(serializer.data)

class ProgrammingLanguageListView(APIView):
	def get(self, request):
		qs = ProgrammingLanguage.objects.all()
		serializer = ProgrammingLanguageSerializer(qs, many=True)
		return Response(serializer.data,headers={"Accept":"application/json; indent=4"})

class TrendingQuestionListView(APIView):
	def get(self, request):
		qs = Question.objects.all().order_by('-likes')[:30]
		serializer = QuestionSerializer(qs, many=True)
		return Response(serializer.data)

class TrendingDeveloperListView(APIView):
	def get(self, request):
		qs = UserProfile.objects.all().order_by('-points').exclude(points=0)[:10]
		serializer = UserProfileSerializer(qs, many=True)
		return Response(serializer.data)

def list_urls(lis, acc=None):
	if acc is None:
		acc = []
	if not lis:
		return
	l = lis[0]
	if isinstance(l, URLPattern):
		yield acc + [str(l.pattern)]
	elif isinstance(l, URLResolver):
		yield from list_urls(l.url_patterns, acc+[str(l.pattern)])
	yield from list_urls(lis[1:], acc)

class OverView(APIView):
	def get(self, request):
		urlconf = __import__("api.urls",{},{},[''])
		data = list_urls(urlconf.urlpatterns)
		data = list(data)
		context = {}
		index = 0
		for i in data:
			context.update({str(index):i})
			index += 1
		return Response(data)

class QuestionDetailView(APIView):
	def get(self, request, *args, **kwargs):
		q = Question.objects.filter(url=kwargs['url'])
		if q.exists():
			serializer = QuestionSerializer(q, many=True)
			return Response(serializer.data)
		else:
			return Response({"error":"Question not found"})