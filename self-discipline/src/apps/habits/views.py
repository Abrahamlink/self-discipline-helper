from django.shortcuts import render
from django.http import HttpResponse


def habits(request):
    return HttpResponse('<h1>Here will be all habits</h1>')
