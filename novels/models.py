from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone


class Novel(models.Model):
    novel_name = models.CharField(max_length=255, default='')
    release_date = models.DateTimeField('date released', default=timezone.now())
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.novel_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.novel_name)
        super(Novel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('novel_page', args=[self.slug])



class Chapter(models.Model):
    chapter_name = models.CharField(max_length=255, default='')
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)

    def __str__(self):
        return self.chapter_name

    class Meta:
        ordering = ('id',)
        unique_together = ('novel', 'chapter_name')
