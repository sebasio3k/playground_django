import logging
from django.shortcuts import render
from minilibrary.models import Author, Book
from django.db.models import Q, F
from django.core.paginator import Paginator

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
        date_start = request.GET.get('start')
        date_end = request.GET.get('end')

        # filters
        if query:
            books = books.filter(
                Q(title__icontains=query) | 
                Q(author__name__icontains=query) | 
                Q(genres__name__icontains=query)
            ).distinct()
            logger.info(f'Query: {query}, Results: {books.count()}')
            
        if date_start and date_end:
            books = books.filter(publication_date__range=[date_start, date_end])
        
        # pagination
        paginator = Paginator(books, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        query_params = request.GET.copy()
        
        if "page" in query_params:
            del query_params["page"]
            
        query_string = query_params.urlencode()
        
        
        return render(request, "minilibrary/index.html", {
            'text': "Minilibrary Page",
            # 'books': books,
            'page_obj': page_obj,
            'query': query,
            "query_string": query_string
        })
    except Exception as e:
        logger.error(f'Error: {e}')
        return render(request, "404.html", status=404)
    
    