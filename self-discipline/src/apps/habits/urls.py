from django.urls import path
from . import views

urlpatterns = [
    path('', views.habits, name='all_habits'),
    path('habit&id=<int:pk>', views.habit_detail, name='habit_detail'),
    path('create_new', views.create_new_habit, name='create_new_habit'),
    path('delete_habit_<int:pk>', views.delete_habit, name='delete_habit'),
    path('complete_day&id=<int:pk>', views.complete_day, name='complete_day'),
]
