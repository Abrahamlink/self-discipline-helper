from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='all_todos'),
    path('done/', views.completed_todos, name='completed_todos'),
    path('create/', views.create_task, name='create_task'),
    path('delete&id=<int:task_id>/', views.delete_task, name='delete_task'),
    path('complete&id=<int:task_id>/', views.complete_task, name='complete_task'),
]
