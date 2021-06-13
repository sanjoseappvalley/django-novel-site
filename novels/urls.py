from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>/', views.novel_page, name='novel_page'),
    path('<slug:slug1>/<slug:slug2>/', views.chapter_page, name='chapter_page'),
]
