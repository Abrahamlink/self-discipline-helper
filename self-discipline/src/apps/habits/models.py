import datetime

from django.contrib.auth.models import User
from django.db import models


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Habit name', max_length=250)
    description = models.TextField('Habit note', blank=True)
    period = models.PositiveIntegerField('Period of setting habit up', default=21)
    category = models.ManyToManyField('Category', blank=True, related_name='habit')
    created = models.DateField(auto_now_add=True)

    def implementation(self):
        all_days = Day.objects.filter(habit=self)
        past_days = [day for day in all_days if day.date < datetime.date.today()]
        if Day.objects.filter(date=datetime.date.today(), habit=self)[0].is_completed:
            past_days.append('completed')
        return [round(len(past_days) / len(all_days) * 100), len(past_days)]

    def is_today_completed(self):
        day = Day.objects.filter(habit=self, date=datetime.date.today())[0]
        return day.is_completed

    class Meta:
        verbose_name = 'Habit'
        verbose_name_plural = 'Habits'
        ordering = ('title',)

    # also make function for check of progress in time

    def __str__(self):
        return self.title


class Day(models.Model):
    is_completed = models.BooleanField(default=False)
    date = models.DateField('Date')
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)

    def today(self):
        return self.date == datetime.date.today()


class Category(models.Model):
    title = models.CharField('Category name', max_length=120, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title
