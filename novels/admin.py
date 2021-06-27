from django.contrib import admin
from .models import Novel, Chapter, Comment

admin.site.register(Novel)
admin.site.register(Chapter)
admin.site.register(Comment)
