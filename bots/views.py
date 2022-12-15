# Create your views here.
from django.shortcuts import render
from . import tasks

def index(request):
    return render(request, 'bots/index.html', {})
