from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, Textarea, DateTimeInput, CharField, PasswordInput, EmailInput
from .models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'is_important', 'deadline']
        widgets = {
            'deadline': DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'When it mast be achieved',
                'name': 'deadline',
                'type': 'datetime-local'
            }),
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Task title',
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Task description',
            }),
        }


class SignUpForm(UserCreationForm):
    username = CharField(label='Username', widget=TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Type username...'
    }))
    email = CharField(label='Email', widget=EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Type email address...'
    }))
    password1 = CharField(label='Password', widget=PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Type password firstly...'
    }))
    password2 = CharField(label='Repeat Password', widget=PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Type password secondly...'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = CharField(label='Username', widget=TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Type username...'
    }))
    password = CharField(label='Password', widget=PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Type password...'
    }))

    class Meta:
        model = User
        fields = ['username', 'password']
