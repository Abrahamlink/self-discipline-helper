from django.forms import ModelForm, TextInput, Textarea, DateInput, DateTimeInput
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
            })}
