from django.shortcuts import render, redirect
from django.conf import settings
from .models import Task
from .forms import TaskForm, SignUpForm, LoginForm
# Auth and Reg
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
import datetime
from zoneinfo import ZoneInfo


def todo_list(request):
    template = 'todo/tasks.html'

    if request.user.is_anonymous:
        return redirect('loginUser')
    try:
        important = Task.objects.filter(user=request.user, finish_date=None, is_important=True).order_by('deadline')
        simple = Task.objects.filter(user=request.user, finish_date=None, is_important=False).order_by('deadline')
        todos = [*important, *simple]
    except TypeError:
        todos = []
    return render(request, template, {'todos': todos})


def completed_todos(request):
    template = 'todo/tasks.html'

    if request.user.is_anonymous:
        return redirect('loginUser')
    else:
        try:
            completed = Task.objects.filter(user=request.user).order_by('-created_date')
        except TypeError:
            completed = []
        filtered_by_finish_date = []
        if len(completed) != 0:
            for todo in completed:
                if todo.finish_date is not None:
                    filtered_by_finish_date.append(todo)

    return render(request, template, {'completed': filtered_by_finish_date})


def create_task(request):
    template = 'todo/create.html'
    helper = {'on': True, 'off': False}

    if not request.user.is_anonymous:
        if request.method == 'GET':
            return render(request, template, context={'form': TaskForm()})
        else:
            try:
                important = helper[request.POST['is_important']]
            except KeyError:
                important = False
            desc = request.POST['description'].split('\r')
            desc = ''.join([string.replace('\n', '<br>') for string in desc])
            new_task = Task(
                title=request.POST['title'],
                description=desc,
                is_important=important,
                user=request.user,
            )
            try:
                date = request.POST['deadline'].split('-')
                day = int(date[2].split(':')[0][:2])
                hour = int(date[2].split(':')[0][-2:])
                minute = int(date[2].split(':')[-1])
                date[2] = day
                new_task.deadline = datetime.datetime(int(date[0]), int(date[1]), date[2], hour, minute)
                new_task.deadline_is_matched = True
            except Exception as e:
                new_task.deadline = datetime.datetime.now()
            new_task.save()
            return redirect('all_todos')
    else:
        return redirect('loginUser')


def delete_task(request, task_id):
    if not request.user.is_anonymous or request.method == 'GET':
        if request.method == 'POST':
            task = Task.objects.get(pk=task_id)
            if task.finish_date is not None:
                link = 'completed_todos'
            else:
                link = 'all_todos'
            task.delete()
        return redirect(link)
    else:
        return redirect('loginUser')


def complete_task(request, task_id):
    if not request.user.is_anonymous or request.method == 'GET':
        if request.method == 'POST':
            task = Task.objects.get(pk=task_id)
            zone = ZoneInfo(settings.TIME_ZONE)
            task.finish_date = datetime.datetime.now(zone)
            task.save()
        return redirect('all_todos')
    else:
        return redirect('loginUser')


"""

For signing up and login on the site

"""


def signUpUser(request):
    template = 'todo/signup.html'
    if request.method == 'GET':
        return render(request, template, context={'form': SignUpForm()})
    elif request.method == 'POST':
        data = {
            'name': request.POST['username'],
            'password1': request.POST['password1'],
            'password2': request.POST['password2'],
            'email': request.POST['email'],
        }
        if data['password1'] == data['password2']:
            try:
                user = User.objects.create_user(username=data['name'], password=data['password1'])
                user.email = data['email']
                user.save()
                if not request.user.is_anonymous:
                    logout(request)
                login(request, user)
                return redirect('all_todos')
            except IntegrityError:
                return render(request, template, context={'form': SignUpForm(),
                                                          'error': "User with that name already exists"})
        else:
            return render(request, template, context={'form': SignUpForm(),
                                                      'error': "Passwords don't match"})


def login_user(request):
    template = 'todo/login.html'
    if request.method == 'GET':
        return render(request, template, context={'form': LoginForm()})
    elif request.method == 'POST':
        if not request.user.is_anonymous:
            try:
                logout(request)
            except:
                pass
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('all_todos')
        else:
            return render(request, template, context={'form': LoginForm(),
                                                      'error': 'Some troubles'})


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('loginUser')
