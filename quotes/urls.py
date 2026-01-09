from django.urls import path
from . import views



urlpatterns = [
    path("", views.index),
    # path("monday", views.monday),
    # path("tuesday", views.tuesday),
    path("<int:day>", views.days_week_with_number, name="days_week_with_number"),
    path("<str:day>", views.days_week, name="days_week"),


]

