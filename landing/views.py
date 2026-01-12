from django.shortcuts import render
from django.http import HttpResponse
from datetime import date

# Create your views here.

def home(request):
    nombre = "sebastian"
    today = date.today()
    stack = ["HTML", "CSS", "JS", "Python", "React", "Django"]
    # stack = []
    
    return render(
        request, 
        "landing/landing.html", 
        {
            "name": nombre,
            "age": 29,
            "today": today,
            "stack": stack
        }
    )