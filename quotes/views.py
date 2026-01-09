import logging
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from inspiring_quotes import get_random_quote
from django.urls import reverse


# Create your views here.

logger = logging.getLogger(__name__)
# logger = logging.getLogger("playground")



DAYS = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]

DAYS_WEEK_WITH_NUMBER = {
    1: "monday",
    2: "tuesday",
    3: "wednesday",
    4: "thursday",
    5: "friday",
    6: "saturday",
    7: "sunday",
}

PHRASES_OF_THE_DAY = {
    "monday": "Pienso, luego existo",
    "tuesday": "La vida es un sueño",
    "wednesday": "El conocimiento es poder",
    "thursday": "Sé el cambio que quieres ver",
    "friday": "Solo sé que no sé nada",
    "saturday": "Vive como si fuera le último dia",
    "sunday": "Da un poquito más todos los días"
}

def index(request):
    list_items = ""
    days = list(PHRASES_OF_THE_DAY.keys())
    
    for day in days:
        day_path = reverse("days_week", args=[day])
        list_items += f"<li><a href=\"{day_path}\">{day.capitalize()}</a></li>"
    
    template = f""" <h1> Hello, world. You're at the quotes index. </h1>
                <ul>        
                    {list_items}
                </ul>
                """ 
    
    return HttpResponse(template)


# def monday(request):
#     return HttpResponse("Hello, today is Monday.")

# def tuesday(request):
#     return HttpResponse("Hello, today is Tuesday.")

def get_quote(day):
    quote = get_random_quote()
    text = ''
    if type(day) == int:
        day = DAYS_WEEK_WITH_NUMBER[day]
    else:
        day = day.lower()
    
    if day == "tuesday":
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
        return HttpResponseNotFound("<h1>Not a valid day of the week.</h1>")
    
    quote_text = get_quote(day)    
    return HttpResponse(f"Hello, today is {day.capitalize()}.\n {quote_text}")

def days_week_with_number(request, day):
    
    try:
        quote_text = get_quote(day)    
        # return HttpResponse(f"Hello, today is {DAYS_WEEK_WITH_NUMBER.get(day).capitalize()}.\n {quote_text}")
        
        # return HttpResponseRedirect("/quotes/index")
        redirect_path = reverse("days_week", args=[DAYS_WEEK_WITH_NUMBER.get(day)])
        logger.info(f"Redirecting to {redirect_path}")
        return HttpResponseRedirect(redirect_path)
        
    except KeyError:
        logger.info(f"Error en days_week_with_number {KeyError}")
        return HttpResponseNotFound("Not a valid number for a day of the week.")
