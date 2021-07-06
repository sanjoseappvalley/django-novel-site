from django.db import models
from django.urls import reverse
from django.utils.text import slugify
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Novel(models.Model):
    novel_name = models.CharField(max_length=255, default='')
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.novel_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.novel_name)
        super(Novel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('novel_page', args=[self.slug])

    class Meta:
        ordering = ('id',)


class Chapter(models.Model):
    chapter_name = models.CharField(max_length=255, default='')
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    content = models.TextField(default='')
    slug = models.SlugField(max_length=255, default=None)

    def __str__(self):
        return self.chapter_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.chapter_name)
        super(Chapter, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('chapter_page', args=[self.novel.slug, self.slug])

    @property
    def number_of_comments(self):
        return Comment.objects.filter(chapter=self).count()

    class Meta:
        ordering = ('id',)
        unique_together = ('novel', 'chapter_name')


class Comment(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user))
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment {self.body} by {self.user}'
