# from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Novel, Chapter, Comment
from .forms import CommentForm

def home_page(request):
    current_novel_list = Novel.objects.all()
    context = {'current_novel_list': current_novel_list}
    return render(request, 'novels/home.html', context)

def novel_page(request, slug):
    novel = get_object_or_404(Novel, slug=slug)
    return render(request, 'novels/novel.html', {'novel': novel})

def chapter_page(request, slug1, slug2):
    novel = get_object_or_404(Novel, slug=slug1)
    chapter = get_object_or_404(Chapter, slug=slug2)
    nextchap = novel.chapter_set.filter(id__gt=chapter.id).order_by('id').first()
    prevchap = novel.chapter_set.filter(id__lt=chapter.id).order_by('id').last()
    comments = chapter.comments.filter(active=True)

    if request.method == 'POST':
        cf = CommentForm(request.POST)
        if cf.is_valid():
            body = request.POST.get('body')
            comment = Comment.objects.create(chapter=chapter, user=request.user, body=body)
            comment.save()
            return redirect(chapter.get_absolute_url())
    else:
        cf = CommentForm()
    return render(request, 'novels/chapter.html', {'novel': novel, 'chapter': chapter, 'nextchap': nextchap, 'prevchap': prevchap, 'comments': comments, 'comment_form': cf})
