import logging
from django.shortcuts import render
from minilibrary.models import Author, Book
from django.db.models import Q, F

logger = logging.getLogger(__name__)

# Create your views here.

def index_1(request):
    try:
        books = Book.objects.all()
        author_id = request.GET.get('author')
        genre_id = request.GET.get('genre')
        author = None
        
        if author_id:
            books = books.filter(author_id=author_id)
            author = Author.objects.get(id=author_id)
            
        if genre_id:
            books = books.filter(genres__id=genre_id)
        
        return render(request, "minilibrary/index.html", {
            'text': "Minilibrary Page index",
            'author_id': author_id,
            'books': books,
            'author': author,
            'genre_id': genre_id
        })
    except Exception as e:
        logger.error(f'Error: {e}')
        return render(request, "404.html", status=404)
    
def index(request):
    try:
        books = Book.objects.all()
        query = request.GET.get('query_search')

        if query:
            books = books.filter(
                Q(title__icontains=query) | 
                Q(author__name__icontains=query) | 
                Q(genres__name__icontains=query)
            ).distinct()
            logger.info(f'Query: {query}, Results: {books.count()}')
        
        return render(request, "minilibrary/index.html", {
            'text': "Minilibrary Page",
            'books': books,
            'query': query,
        })
    except Exception as e:
        logger.error(f'Error: {e}')
        return render(request, "404.html", status=404)
    
    