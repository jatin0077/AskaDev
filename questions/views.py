from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import CreateView, ListView
from accounts.models import UserProfile
from .models import Question, Answer, Liker, AnswerLiker
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import secrets, json

@csrf_exempt
def likeAnswer(request):
	if request.method == 'POST':
		post = request.POST.get('answer')
		user = request.POST.get('user')
		liked = AnswerLiker.objects.filter(
			user=User.objects.get(username=user),
			Answer=Answer.objects.get(url=post)
		).exists()
		if not liked:
			l = AnswerLiker(
				user=User.objects.get(username=user),
				answer=Answer.objects.get(url=post),
				liked=True
			)
			l.save()
			p = Answer.objects.get(url=post)
			p.likes += 1
			p.save()
		else:
			l = AnswerLiker.objects.get(user=User.objects.get(username=user),question=Question.objects.get(url=post))
			l.delete()
			p = Answer.objects.get(url=post)
			p.likes -= 1
			p.save()
		return HttpResponse(liked)
	else:
		return redirect('/')
@csrf_exempt
def likePost(request):
	if request.method == 'POST':
		js = json.loads(request.body.decode("utf-8"))
		post = js['question']
		user = js['user']
		print(js)
		print(user)
		print(post)
		liked = Liker.objects.filter(
			user=User.objects.get(username=user),
			question=Question.objects.get(url=post)
		).exists()
		if not liked:
			l = Liker(
				user=User.objects.get(username=user),
				question=Question.objects.get(url=post),
				liked=True
			)
			l.save()
			p = Question.objects.get(url=post)
			p.likes += 1
			asked_by = Question.objects.get(url=post).user
			up = UserProfile.objects.get(user=asked_by)
			up.points += 1
			up.save()
			p.save()
		else:
			l = Liker.objects.get(user=User.objects.get(username=user),question=Question.objects.get(url=post))
			l.delete()
			p = Question.objects.get(url=post)
			p.likes -= 1
			asked_by = Question.objects.get(url=post).user
			up = UserProfile.objects.get(user=asked_by)
			up.points -= 1
			up.save()
			p.save()
		return HttpResponse(liked)
	else:
		return redirect('/')
def QuestionDetailView(request, user, question):
	user = get_object_or_404(User, username=user)
	question = get_object_or_404(Question,user=user, url=question)
	context = {"user":user, "question":question}
	answers = Answer.objects.filter(question=question).order_by('-answered_at')
	context['answers'] = answers
	liked = Liker.objects.filter(user=User.objects.get(username=request.user),question=question).exists()
	print(liked)
	context['liked'] = liked
	return render(request, "questions/question_detail.html",context=context )

class QuestionCreateView(CreateView):
	model = Question
	fields = ('title','question','tags')
	success_url = ''
	def form_valid(self,form):
		tags = form.cleaned_data.get('tags')
		user=User.objects.get(username=self.request.user.username)
		q = Question(
			user=User.objects.get(username=self.request.user.username),
			title=form.cleaned_data.get('title'),
			question=form.cleaned_data.get('question'),
			url=secrets.token_hex(20)
		)
		q.save()
		for i in tags.iterator():
			q.tags.add(i)
		q.save()
		return redirect(f'/{user}/questions/{q.url}')

class AnswerCreateView(CreateView):
	model = Answer
	fields = ('answer',)

	def form_valid(self, form):
		answer = form.cleaned_data.get('answer')
		user=User.objects.get(username=self.request.user.username)
		user_profile = UserProfile.objects.get(user=user)
		question = get_object_or_404(Question,url=self.kwargs['question'])
		a = Answer(
			question=question,
			answered_by=user,
			url=secrets.token_hex(20),
			answer=answer,
		)
		a.save()
		user_profile.points += 1
		user_profile.save()
		slug = question.url
		return redirect(f'/{question.user}/questions/{slug}')

class TrendingQuestionView(ListView):
	model = Question

	def get_queryset(self, *args, **kwargs):
		qs = Question.objects.all().order_by('-likes')[:30]
		return qs