from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField('Task title', max_length=250)
    description = models.TextField('Note for task', blank=True)
    deadline = models.DateTimeField('When it mast be achieved', blank=True, null=True)
    created_date = models.DateTimeField('Date of creating task', auto_now_add=True)
    finish_date = models.DateTimeField('Finish date', null=True, blank=True)
    deadline_is_matched = models.BooleanField(default=False)
    is_important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ('title',)

    def __str__(self):
        return self.title

    def is_task_date_left(self):
        return self.deadline < timezone.now()
