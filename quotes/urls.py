from django.urls import path
from . import views



urlpatterns = [
    path("index", views.index),
    path("monday", views.monday),
    path("tuesday", views.tuesday),


]

