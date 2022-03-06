from django.forms import ModelForm, TextInput, Textarea, NumberInput
from .models import Habit


class HabitForm(ModelForm):
    class Meta:
        model = Habit
        fields = ['title', 'description']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Habit title',
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Habit description',
            }),
        }