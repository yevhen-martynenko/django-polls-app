import re

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404

from .forms import PollForm
from .models import Poll, Question, Option


@login_required()
def main(request):
    is_all_polls = bool(request.GET.get('all', True))

    if is_all_polls:
        item_list = Poll.objects.filter(active=True).order_by('date_of_creation')
    else:
        item_list = Poll.objects.filter(owner=request.user, active=True)

    search_term = ''

    if 'search' in request.GET:
        search_term = request.GET['search']
        item_list = item_list.filter(title__icontains=search_term)

    page = {
        'list': item_list,
        'search_term': search_term,
        'title': 'Poll List' if is_all_polls else 'User Poll List',
    }

    return render(request, 'core/polls.html', page)


@login_required()
def remove(request, code):
    item = get_object_or_404(Poll, code=code)
    if item.owner == request.user:
        item.delete()
        messages.info(request, 'Poll has been removed')
    else:
        messages.info(request, 'You can not remove other users poll')
    return redirect('core:main')


@login_required()
def create(request):
    password = ''
    
    if request.method == 'POST':
        form = PollForm(request.POST)
        form.user = request.user
        if form.is_valid():
            password = request.POST.get('password')
            poll = form.save()
            if password:
                poll.public = False
                poll.password = password
                poll.save() 
            question_text_data = request.POST.getlist('question_text')
            question_type_data = request.POST.getlist('question_type')
            for i, question_text in enumerate(question_text_data):
                question_type = question_type_data[i]
                required = bool(request.POST.get(f'required{i}'))
                question = Question.objects.create(poll=poll, question_text=question_text, question_type=question_type, required=required)
                if question_type != 'SHORT_TEXT' and question_type != 'LONG_TEXT':
                    option_field = f'options_{i}'
                    option_data = request.POST.getlist(option_field)
                    for option_text in option_data:
                        option = Option.objects.create(question=question, option_text=option_text)
            return redirect('core:main')
    else:
        form = PollForm()

    page = {
        'poll': form,
        'password': password,
        'title': 'Create Poll',
    }

    return render(request, 'core/create.html', page)


@login_required
def vote(request, code):
    request.session['confirmed_password'] = False
    if request.method == 'POST':
        poll = get_object_or_404(Poll, code=code)
        
        is_public = poll.public
        if not is_public:
            entered_password = request.POST.get('password', '')
            if entered_password == poll.password:
                request.session['confirmed_password'] = True
            else:
                messages.info(request, 'Invalid password')
                return redirect(request.path_info)
    
        # TODO check if all required questions are answered
        for index, question in enumerate(poll.question_set.all()):
            if question.question_type == 'SHORT TEXT':
                answer = request.POST.get(f'short-text-{index}')
                if answer:
                    option = Option.objects.create(question=question, text_answer=answer)
                    question.total_answers += 1
                    question.save()
            elif question.question_type == 'LONG TEXT':
                answer = request.POST.get(f'long-text-{index}')
                if answer:
                    option = Option.objects.create(question=question, text_answer=answer)
                    question.total_answers += 1
                    question.save()
            elif question.question_type == 'CHECKBOX':
                answered = False
                for i in range(len(question.option_set.all())):
                    selected_option_id = request.POST.get(f'q{index}-check{i}')
                    if selected_option_id:
                        try:
                            option = question.option_set.all()[i]
                            option.votes += 1
                            answered = True
                            option.save()
                        except IndexError:
                            raise Http404("Option not found")
                if answered:
                    question.total_answers += 1
                    question.save()
            elif question.question_type == 'RADIO':
                selected_option_id = request.POST.get(f'q{index}-options') 
                option_id = int(re.findall(r'\d+$', selected_option_id)[0])
                try:
                    option = question.option_set.all()[option_id]
                    option.votes += 1
                    question.total_answers += 1
                    option.save()
                    question.save()
                except IndexError:
                    raise Http404("Option not found")

        return redirect('core:results', code=code)
    else:
        poll = get_object_or_404(Poll, code=code)
        confirmed_password = request.session.get('confirmed_password', False)

        poll_data = {
            'code': poll.code,
            'title': poll.title,
            'description': poll.description,
            'date_of_creation': poll.date_of_creation,
            'user': request.user,
            'owner': poll.owner,
            'active': poll.active,
            'public': poll.public,
            'questions': [],
        }

        poll_questions = poll.question_set.all()
        for question in poll_questions:
            question_data = {
                'question_text': question.question_text,
                'question_type': question.question_type,
                'required': question.required,
                'options': [],
            }

            question_options = question.option_set.all()
            for option in question_options:
                question_data['options'].append(option.option_text)
            poll_data['questions'].append(question_data)

        page = {
            'poll': poll_data,
            'confirmed_password': confirmed_password,
            'title': 'Vote Poll',
        }

        return render(request, 'core/vote.html', page)


@login_required
def results(request, code):
    poll = get_object_or_404(Poll, code=code)
    poll_data = {
        'code': poll.code,
        'title': poll.title,
        'description': poll.description,
        'date_of_creation': poll.date_of_creation,
        'user': request.user,
        'owner': poll.owner,
        'active': poll.active,
        'public': poll.public,
        'questions': [],
    }

    poll_questions = poll.question_set.all()
    for question in poll_questions:
        question_data = {
            'question_text': question.question_text,
            'question_type': question.question_type,
            'required': question.required,
            'total_answers': question.total_answers,
            'options': [],
        }

        question_options = question.option_set.all()
        for option in question_options:
            option_data = {
                'option_text': option.option_text,
                'votes': option.votes,
                'text_answer': option.text_answer,
            }
            question_data['options'].append(option_data)
        poll_data['questions'].append(question_data)

    page = {
        'poll': poll_data,
        'title': 'Poll Results',
    }

    return render(request, 'core/results.html', page)


@login_required
def edit(request, code):
    poll = get_object_or_404(Poll, code=code)

    page = {
        'poll': poll,
        'title': 'Edit Poll',
    }

    return render(request, 'stub.html', page)
    # return render(request, 'core/edit.html', page)
