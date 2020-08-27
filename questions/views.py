from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import CreateView, ListView
from .models import Question, Answer, Liker
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import secrets
@csrf_exempt
def likePost(request):
	if request.method == 'POST':
		post = request.POST.get('question')
		user = request.POST.get('user')
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
			p.save()
		else:
			l = Liker.objects.get(user=User.objects.get(username=user),question=Question.objects.get(url=post))
			l.delete()
			p = Question.objects.get(url=post)
			p.likes -= 1
			p.save()
			print("Here")
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
        question = get_object_or_404(Question,url=self.kwargs['question'])
        a = Answer(
            question=question,
            answered_by=user,
            url=secrets.token_hex(20),
            answer=answer,
        )
        a.save()
        slug = question.url
        return redirect(f'/{question.user}/questions/{slug}')

class TrendingQuestionView(ListView):
    model = Question

    def get_queryset(self, *args, **kwargs):
        qs = Question.objects.all().order_by('-likes')[:30]
        return qs