#articles/____  이후의 경로!!

from django.urls import path
from . import views
urlpatterns = [
    path('index/', views.index),
    path('new/', views.new),
    path('create/', views.create),
]
