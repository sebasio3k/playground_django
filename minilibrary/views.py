import logging
import time
from django.shortcuts import render, redirect, get_object_or_404
from minilibrary.models import Author, Book
from django.db.models import Q, F
from django.core.paginator import Paginator
from .forms import ReviewSimpleForm, ReviewForm
from .models import Review
from django.contrib.auth import get_user_model
from django.contrib import  messages
from django.http import HttpResponse, HttpResponseForbidden
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin



logger = logging.getLogger(__name__)
User = get_user_model()

# Create your views here.

# FBV
def hello(request):
    return HttpResponse("Hello World from FBV")

# CBV
class Hello(View):
    def get(self, request):
        return HttpResponse("Hello World from CBV")
    

class WelcomeView(TemplateView):
    template_name = "minilibrary/welcome.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Minilibrary"
        context['total_books'] = Book.objects.count()
        return context
    

class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = "minilibrary/book_list.html"
    context_object_name = "books"
    paginate_by = 5
    

class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = "minilibrary/book_detail.html"
    context_object_name = "book"
    # slug_field = "slug"
    # slug_url_kwarg = "slug"
    
    def get(self, request, *args, **kwargs):
        if request.user.has_perm('minilibrary.view_book'):
            response = super().get(request, *args, **kwargs)
            request.session['last_viewed_book'] = self.object.id
            return response
        else:
            return HttpResponseForbidden("No tienes permiso para ver este libro.")

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "minilibrary/review_create.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = Book.objects.get(pk=self.kwargs['pk'])
        context['book_reviews'] = Review.objects.filter(book=self.kwargs['pk'], user_id=self.request.user.id)
        return context
    
    def form_valid(self, form):
        book_id = self.kwargs['pk']
        book = Book.objects.get(pk=book_id)
        form.instance.book = book
        form.instance.user_id = self.request.user.id
        messages.success(self.request, "Gracias por la reseña")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('create-review', kwargs={'pk': self.kwargs['pk']})

class ReviewUpdateView(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "minilibrary/review_create.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = Book.objects.get(pk=self.kwargs['book_id'])
        context['book_reviews'] = Review.objects.filter(
            book=self.kwargs['book_id'])
        context['text_update'] = "Actualizar reseña"
        return context
    
    def get_queryset(self):
        return Review.objects.filter(user_id=self.request.user.id)

    def form_valid(self, form):
        messages.success(self.request, "Se ha actualizado la reseña correctamente.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al actualizar la reseña.")
    
    def get_success_url(self):
        return reverse_lazy('create-review', kwargs={'pk': self.object.book_id})

class ReviewDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'minilibrary.delete_review'
    model = Review
    template_name = "minilibrary/review_confirm_delete.html"
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = Book.objects.get(pk=self.kwargs['book_id'])
        return context
    
    def get_success_url(self):
        return reverse_lazy('create-review', kwargs={'pk': self.kwargs['book_id']})
    
    def get_queryset(self):
        return Review.objects.filter(user_id=self.request.user.id)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Se ha eliminado la reseña correctamente.")
        return super().delete(request, *args, **kwargs)
    
        

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
    
@login_required # for fbv
def index(request):
    try:
        books = Book.objects.all()
        query = request.GET.get('query_search')
        date_start = request.GET.get('start')
        date_end = request.GET.get('end')
        book_id_recommend = request.session.get('last_viewed_book')


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
        
        if book_id_recommend:
            try:
                last_book = Book.objects.get(id=book_id_recommend)
            except Book.DoesNotExist:
                last_book = None
        else:
            last_book = None
        
        
        return render(request, "minilibrary/index.html", {
            'text': "Minilibrary Page",
            # 'books': books,
            'page_obj': page_obj,
            'query': query,
            "query_string": query_string,
            'last_book': last_book,
        })
    except Exception as e:
        logger.error(f'Error: {e}')
        return render(request, "404.html", status=404)
    
    
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    form = ReviewSimpleForm(request.POST or None)
    book_reviews = Review.objects.filter(book=book)
    
    if request.method == "POST":
        if form.is_valid():
            rating = form.cleaned_data['rating']
            text = form.cleaned_data['text']
            user = request.user if request.user.is_authenticated else User.objects.first()
            
            Review.objects.create(
                user=user,
                book=book,
                rating=rating,
                text=text
            )
            
            messages.success(request, "Gracias por la reseña")
            return redirect('recommend_book', book_id=book.id)
        else:
            messages.error(request, "Corrija los errores de la reseña")
        
    return render(request, "minilibrary/add_review.html", {
        'book': book,
        'form': form,
        'book_reviews': book_reviews
    })
    

# Con ModelForm
@permission_required('minilibrary.add_review')
def add_review_form(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    form = ReviewForm(request.POST or None)
    book_reviews = Review.objects.filter(book=book)
    
    if request.method == "POST":
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            # review.user = request.user if request.user.is_authenticated else User.objects.first()
            review.save()
            
            messages.success(request, "Gracias por la reseña")
            return redirect('recommend_book_form', book_id=book.id)
        else:
            messages.error(request, "Corrija los errores de la reseña", extra_tags='danger')
        
    return render(request, "minilibrary/add_review_form.html", {
        'book': book,
        'form': form,
        'book_reviews': book_reviews
    })
        

def Home(request):
    time.sleep(2)
    print(request.user)
    return HttpResponse("Hello World from Home")
    

def visit_counter(request):
    visits_count = request.session.get('visit_count', 0)
    visits_count += 1
    request.session['visit_count'] = visits_count
    # request.session.set_expiry(15)
    # 300 = 5 min, 0 = close navigation, None = no expire
    return HttpResponse(f"You have visit this page {visits_count} times.")

