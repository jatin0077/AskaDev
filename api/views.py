from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserProfileSerializer, ProgrammingLanguageSerializer, QuestionSerializer
from accounts.models import UserProfile, ProgrammingLanguage
from questions.models import Question
from django.conf import settings
import json
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
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


class CanLogin(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
	 return super(CanLogin, self).dispatch(request, *args, **kwargs)

	def post(self, request):
		data = {"canLogin": "False"}
		username = request.POST.get('username') or None
		password = request.POST.get('password') or None

		u = User.objects.filter(username=username)
		if u.exists():
			u = u[0]
			if u.check_password(password):
				data['canLogin'] = 'True'
		return JsonResponse(data)


class GetUserProfile(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(GetUserProfile, self).dispatch(request, *args, **kwargs)

	def post(self, request):
	    received_json_data = json.loads(request.body.decode('utf-8'))
	    pk = received_json_data["pk"]
	    user_profile = UserProfile.objects.filter(id=pk)
	    if user_profile.exists():
	        user_profile = user_profile[0]
	        data = UserProfileSerializer(user_profile, many=False)
	        data = data.data
	    else:
	       data = {"error":"User does not exist"}
	    return JsonResponse(data)


class GetLanguage(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(GetLanguage, self).dispatch(request, *args, **kwargs)

	def post(self, request):
	    received_json_data = json.loads(request.body)
	    pk = received_json_data["pk"]
	    language = ProgrammingLanguage.objects.filter(id=pk)
	    if language.exists():
	        language = language[0]
	        data = ProgrammingLanguageSerializer(language, many=False)
	        data = data.data
	    else:
	        data = {"error":"User does not exist"}
	    return JsonResponse(data)