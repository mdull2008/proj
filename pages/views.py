from django.shortcuts import render

from .models import Skill


def home(request):
    skills = Skill.objects.filter(is_active=True)
    return render(request, 'pages/home.html', {'skills': skills})
