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
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup

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
		data = serializer.data
		question_code = ''
		for i in range(len(data)):
			print(i)
			question_code = repr(BeautifulSoup(data[i]['question'], features='html.parser').text)
			data[i]['question'] = question_code
		return Response(data)

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
			qw = Question.objects.get(url=kwargs['url'])
			serializer = QuestionSerializer(q, many=True)
			data = serializer.data
			question_code = repr(BeautifulSoup(data[0]['question'], features='html.parser').text)
			data[0]['question'] = question_code
			return Response(data)
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

class RegisterUser(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(RegisterUser, self).dispatch(request, *args, **kwargs)

	def post(self, request):
		data = json.loads(request.body) or None
		username = data['username'] or None
		password = data['password'] or None
		data = {}
		if username is not None and password is not None:
			filter_user = User.objects.filter(username=username)
			if filter_user.exists():
				data['status'] = "Invalid"
				data['error'] = 'User Already Exists'
				return JsonResponse(data)
			if len(password) >= 8:
				user = User.objects.create_user(username=username, password=password)
				data['status'] = 'Created'
				data['error'] = 'None'
			else:
				data['status'] = 'Invalid'
				data['error'] = 'Invalid Credentials'
		else:
			data['status'] = 'Invalid'
			data['error'] = 'No Credentials'
		return JsonResponse(data)


class GetQuestionsByUser(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
	 return super().dispatch(request, *args, **kwargs)

	def post(self, request):
		body = request.body or None
		if body == None:
			return JsonResponse({})
		r_body = json.loads(body) or None
		if r_body == None:
			return JsonResponse({})
		username = r_body['username'] or None
		if username != None:
			user = User.objects.filter(username=username)
			if user.exists():
				questions = Question.objects.filter()
				serializer = QuestionSerializer(questions, many=True)
				data = serializer.data
				for i in range(len(data)):
					print(i)
					question_code = repr(BeautifulSoup(data[i]['question'], features='html.parser').text)
					data[i]['question'] = question_code
				return JsonResponse(serializer.data, safe=False)
			else:
				return JsonResponse({"error":"User does not exists"})
		else:
			return JsonResponse({})
