from django.shortcuts import render, redirect
from .models import *
from .forms import HabitForm
import datetime


def habits(request):
    template = 'habits/habits.html'

    if not request.user.is_anonymous:
        practice = Habit.objects.filter(user=request.user).order_by('-created')
    else:
        return redirect('loginUser')
    return render(request, template, context={'habits': practice})


def create_new_habit(request):
    if not request.user.is_anonymous:
        if request.method == 'GET':
            template = 'habits/create.html'
            return render(request, template, context={'form': HabitForm()})
        else:
            desc = request.POST['description'].split('\r')
            desc = ''.join([string.replace('\n', '<br>') for string in desc])
            habit = Habit()
            habit.user = request.user
            habit.title = request.POST['title']
            habit.description = desc
            habit.period = int(request.POST['period'])
            habit.save()
            for index in range(0, habit.period):
                day = Day()
                day.habit = habit
                day.date = datetime.date.today() + datetime.timedelta(index)
                day.save()
            return redirect('all_habits')
    else:
        return redirect('loginUser')


def delete_habit(request, pk):
    if request.method == 'POST':
        if not request.user.is_anonymous:
            habit = Habit.objects.get(pk=pk)
            habit.delete()
            return redirect('all_habits')


def habit_detail(request, pk):
    if not request.user.is_anonymous:
        template = 'habits/habit_details.html'
        habit = Habit.objects.get(user=request.user, pk=pk)
        days = Day.objects.filter(habit=habit)
    else:
        return redirect('loginUser')
    return render(request, template, context={
                                            'habit': habit,
                                            'days': zip(range(1, habit.period + 1), days),
                                            'today': datetime.date.today(),
                                        })


def complete_day(request, pk):
    if request.method == 'POST':
        if not request.user.is_anonymous:
            day = Day.objects.get(pk=pk)
            if day.date > datetime.date.today():
                return redirect('habit_detail', day.habit.pk)
            day.is_completed = True
            day.save()
            return redirect('habit_detail', day.habit.pk)
        else:
            return redirect('loginUser')
