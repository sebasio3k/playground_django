from django.shortcuts import render

# Create your views here.

def index(request):
    try:
        return render(request, "minilibrary/index.html", {
            'text': "Minilibrary Page index"
        })
    except:
        return render(request, "404.html", status=404)