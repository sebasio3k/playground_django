from django.shortcuts import render
from django.http import HttpResponse
from datetime import date

# Create your views here.

def home(request):
    nombre = "sebastian"
    today = date.today()
    # stack = ['HTML', 'CSS', 'JS', 'Python', 'React', 'Django']
    # stack = []
    stack = [{'id': 'html', 'name': 'HTML'}, {'id': 'css', 'name': 'CSS'}, {'id': 'js', 'name': 'JS'}, {
        'id': 'python', 'name': 'Python'}, {'id': 'react', 'name': 'React'}, {'id': 'django', 'name': 'Django'}]
    
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
    
def stack_datail(request, tool):
    return HttpResponse(f"Tecnología: {tool}")
