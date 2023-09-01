from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from users.utils import paginate
from .models import Question, Vote


@login_required
def questions(request):
    profile = request.user.profile

    questions = Question.objects.all()

    custom_range, questions = paginate(request, questions, 3)

    context = {
        'questions': questions,
        'custom_range': custom_range,
        'profile': profile
    }

    return render(request, 'polls/questions.html', context)


@login_required
def question(request, question_id):
    profile = request.user.profile

    question = Question.objects.get(pk=question_id)

    context = {
        'question': question,
        'profile': profile
    }

    return render(request, 'polls/question.html', context)


@login_required
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    votes = question.choice_set.select_related('question').all()

    profile = request.user.profile

    labels = []

    data = []

    for item in votes:
        labels.append(item.name)
        data.append(item.votes)

    context = {
        'question': question,
        'profile': profile,
        'labels': labels,
        'data': data
    }

    return render(request, 'polls/results.html', context)


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    profile = request.user.profile

    try:
        user_choice = question.choice_set.get(pk=request.POST['choice'])

        if not question.user_voted(request.user):
            messages.error(request, 'Вы уже голосовали в этом опросе.')

            context = {
                'question': question,
                'profile': profile
            }

            return render(request, 'polls/question.html', context)

        if user_choice:
            user_choice.votes += 1
            user_choice.save()

            vote = Vote(user=request.user, question=question, choice=user_choice)
            vote.save()

            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    except (KeyError, UnboundLocalError):
        messages.error(request, 'Вы не выбрали вариант ответа!')

        context = {
            'question': question
        }

        return render(request, 'polls/question.html', context)

    context = {
        'question': question,
        'profile': profile
    }

    return render(request, 'polls/results.html', context)
