from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
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

# def monday(request):
#     return HttpResponse("Hello, today is Monday.")

# def tuesday(request):
#     return HttpResponse("Hello, today is Tuesday.")

def get_quote(day):
    quote = get_random_quote()
    text = ''
    
    if day.lower() == "tuesday":
        text = "No quotes available today."
        print(text)
    elif quote:
        text = f"Quote: {quote['quote']}\nAuthor: {quote['author']}"
        print(text)
    else:
        text = "No quotes found."
        print(text)
    
    return text

def days_week(request, day):
    if day.lower() not in DAYS:
        return HttpResponseNotFound("Not a valid day of the week.")
    
    quote_text = get_quote(day)    
    return HttpResponse(f"Hello, today is {day.capitalize()}.\n {quote_text}")

