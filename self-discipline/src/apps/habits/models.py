from django.contrib.auth.models import User
from django.db import models


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Habit name', max_length=250)
    description = models.TextField('Habit note', blank=True)
    period = models.PositiveIntegerField('Period of setting habit up', default=21)
    category = models.ManyToManyField('Category', blank=True, related_name='habit')
    created = models.DateField(auto_now=True)

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


class Category(models.Model):
    title = models.CharField('Category name', max_length=120, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title
