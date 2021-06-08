from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Novel(models.Model):
    novel_name = models.CharField(max_length=255)
    release_date = models.DateTimeField('date released')
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.novel_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.novel_name)
        super(Novel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('novel_page', args=[self.slug])
