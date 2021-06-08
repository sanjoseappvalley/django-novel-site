from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>/', views.novel_page, name='novel_page'),
]
