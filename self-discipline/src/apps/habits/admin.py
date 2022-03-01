from django.contrib import admin
from .models import Habit, Category, Day


class HabitAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'period')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Habit, HabitAdmin)
admin.site.register(Category, CategoryAdmin)
