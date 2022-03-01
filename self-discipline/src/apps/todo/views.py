from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
# Auth and Reg
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone
import datetime


def todo_list(request):
    template = 'todo/tasks.html'

    if request.user.is_anonymous:
        return redirect('signUpUser')
    try:
        todos = Task.objects.filter(user=request.user, finish_date=None).order_by('-created_date')
    except TypeError:
        todos = []
    return render(request, template, {'todos': todos, 'user': request.user})


def completed_todos(request):
    template = 'todo/tasks.html'

    if request.user.is_anonymous:
        return redirect('signUpUser')
    try:
        completed = Task.objects.filter(user=request.user).order_by('-created_date')
    except TypeError:
        completed = []
    filtered_by_finish_date = []
    if len(completed) != 0:
        for todo in completed:
            if todo.finish_date is not None:
                filtered_by_finish_date.append(todo)

    return render(request, template, {'completed': filtered_by_finish_date, 'user': request.user})


def create_task(request):
    template = 'todo/create.html'
    helper = {'on': True, 'off': False}

    if request.method == 'GET':
        return render(request, template, context={'form': TaskForm()})
    else:
        if not request.user.is_anonymous:
            print(request.POST)
            new_task = Task(
                title=request.POST['title'],
                description=request.POST['description'],
                is_important=helper[request.POST['is_important']],
                user=request.user,
            )
            date = request.POST['deadline'].split('-')
            day = int(date[2].split(':')[0][:2])
            hour = int(date[2].split(':')[0][-2:])
            minute = int(date[2].split(':')[-1])
            date[2] = day
            print(date, hour, minute)
            new_task.deadline = datetime.datetime(int(date[0]), int(date[1]), date[2], hour, minute)
            new_task.save()
        return redirect('all_todos')


def delete_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(pk=task_id)
        if task.finish_date is not None:
            link = 'completed_todos'
        else:
            link = 'all_todos'
        task.delete()
    return redirect(link)


def complete_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(pk=task_id)
        task.finish_date = datetime.datetime.now()
        task.save()
    return redirect('all_todos')


# for signing up and login
def signUpUser(request):
    template = 'todo/signup.html'
    if request.method == 'GET':
        return render(request, template, context={'form': UserCreationForm()})
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
                login(request, user)
                return redirect('all_todos')
            except IntegrityError:
                return render(request, template, context={'form': UserCreationForm(),
                                                          'error': "User with that name already exists"})
        else:
            return render(request, template, context={'form': UserCreationForm(),
                                                      'error': "Passwords don't match"})


def login_user(request):
    template = 'todo/login.html'
    if request.method == 'GET':
        return render(request, template, context={'form': AuthenticationForm()})
    elif request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('all_todos')
        else:
            return render(request, template, context={'form': AuthenticationForm(),
                                                      'error': 'Some troubles'})


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('signUpUser')
