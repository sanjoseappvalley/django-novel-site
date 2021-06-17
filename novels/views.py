# from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Novel, Chapter
from django.core.paginator import Paginator

def home_page(request):
    current_novel_list = Novel.objects.all()
    context = {'current_novel_list': current_novel_list}
    return render(request, 'home.html', context)


def novel_page(request, slug):
    novel = get_object_or_404(Novel, slug=slug)
    return render(request, 'novel.html', {'novel': novel})

def chapter_page(request, slug1, slug2):
    novel = get_object_or_404(Novel, slug=slug1)
    chapter = get_object_or_404(Chapter, slug=slug2)
    nextchap = novel.chapter_set.filter(id__gt=chapter.id).order_by('id').first()
    prevchap = novel.chapter_set.filter(id__lt=chapter.id).order_by('id').last()
    return render(request, 'chapter.html', {'novel': novel, 'chapter': chapter, 'nextchap': nextchap, 'prevchap': prevchap})
