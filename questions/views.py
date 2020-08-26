from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import CreateView, ListView
from .models import Question, Answer
import secrets
def QuestionDetailView(request, user, question):
    user = get_object_or_404(User, username=user)
    question = get_object_or_404(Question,user=user, url=question)
    context = {"user":user, "question":question}
    answers = Answer.objects.filter(question=question).order_by('-answered_at')
    context['answers'] = answers
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