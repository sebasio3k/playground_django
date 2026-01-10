from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    nombre = "Sebastian"
    
    return render(
        request, 
        "landing/landing.html", 
        {
            "name": nombre,
            "age": 29
        }
    )