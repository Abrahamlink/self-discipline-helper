import datetime

from django.shortcuts import render, redirect
from .models import *
from .forms import HabitForm
from django.contrib.auth.models import User


def habits(request):
    template = 'habits/habits.html'

    if not request.user.is_anonymous:
        practice = Habit.objects.filter(user=request.user).order_by('-created')
    else:
        practice = []
        return redirect('loginUser')
    return render(request, template, context={'habits': practice})


def create_new_habit(request):
    template = 'habits/create.html'

    if not request.user.is_anonymous:
        if request.method == 'GET':
            return render(request, template, context={'form': HabitForm()})
        else:
            habit = Habit()
            habit.user = request.user
            habit.title = request.POST['title']
            habit.description = request.POST['description']
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


def habit_detail(request, pk):
    template = 'habits/habit_details.html'

    if not request.user.is_anonymous:
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
