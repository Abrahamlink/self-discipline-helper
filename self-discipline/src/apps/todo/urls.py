from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='all_todos'),
    path('create', views.create_task, name='create_task'),
    path('delete&id=<int:task_id>', views.delete_task, name='delete_task'),
]
