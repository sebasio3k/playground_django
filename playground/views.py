# core/views.py
from django.shortcuts import render
from django.urls import get_resolver, URLPattern, URLResolver

# EXCLUDE_PREFIXES = ("admin/",)  # puedes agregar "static/", "media/" si aplica
EXCLUDE_PREFIXES = ()  # puedes agregar "static/", "media/" si aplica

def home(request):
    resolver = get_resolver()
    links = []

    for p in resolver.url_patterns:
        # Solo rutas "top-level" incluidas, ej: quotes/, landings/, minilibrary/
        if isinstance(p, URLResolver):
            prefix = str(p.pattern)  # ej: 'quotes/'
            if prefix and not prefix.startswith(EXCLUDE_PREFIXES):
                links.append({"name": prefix.rstrip("/"), "url": f"/{prefix}"})

        # Si también quieres URLs directas en root (path("algo/", ...))
        elif isinstance(p, URLPattern):
            prefix = str(p.pattern)
            if prefix and not prefix.startswith(EXCLUDE_PREFIXES):
                links.append({"name": p.name or prefix.rstrip("/"), "url": f"/{prefix}"})

    links.sort(key=lambda x: x["name"].lower())
    return render(request, "home.html", {"links": links})