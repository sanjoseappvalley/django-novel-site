# from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Novel


def home_page(request):
    current_novel_list = Novel.objects.all()
    context = {'current_novel_list': current_novel_list}
    return render(request, 'home.html', context)


def novel_page(request, novel_name):
    novel = get_object_or_404(Novel, novel_name=novel_name)
    return render(request, 'novel.html', {'novel': novel})
