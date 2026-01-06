from django.shortcuts import render
from django.http import HttpResponse
from inspiring_quotes import get_random_quote


# Create your views here.

DAYS = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]

def index(request):
    return HttpResponse("Hello, world. You're at the quotes index.")

def monday(request):
    quote = get_random_quote()
    text = ''
    
    if quote:
        text = f"Quote: {quote['quote']}\nAuthor: {quote['author']}"
        print(f"Quote: {quote['quote']}\nAuthor: {quote['author']}")
    else:
        text = "No quotes available."
        print("No quotes available.")
    return HttpResponse(f"Hello, today is Monday.\n {text}")

def tuesday(request):
    return HttpResponse("Hello, today is Tuesday.")


