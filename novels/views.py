# from django.http import HttpResponse
from django.shortcuts import render
from .models import Novel


def home_page(request):
    current_novel_list = Novel.objects.all()
    context = {'current_novel_list': current_novel_list}
    return render(request, 'home.html', context)


def novel_page(request):
    pass
