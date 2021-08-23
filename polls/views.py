from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from .models import Question , Choice
from django.urls import reverse
from django.views import generic
from django.utils import timezone


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request , question_id):
    question  = get_object_or_404(Question , pk = question_id , pub_date__lte=timezone.now() )
    try:
        selected_choice = question.options.get(pk = request.POST['choice'])
    except (KeyError , Choice.DoesNotExist):
        return render(request , 'polls/detail.html' , {'question': question , 'error_message':"you did not select any choice"})
    else:
        selected_choice.votes+=1
        selected_choice.save()
        return  HttpResponseRedirect(reverse('polls:results' , args = (question.id,)))