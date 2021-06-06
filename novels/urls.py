from django.urls import path
from . import views

urlpatterns = [
    path('<novel_name>/', views.novel_page, name='novel_page'),
]
