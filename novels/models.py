from django.db import models

# Create your models here.


class Novel(models.Model):
    novel_name = models.CharField(max_length=200)
    release_date = models.DateTimeField('date released')

    def __str__(self):
        return self.novel_name
