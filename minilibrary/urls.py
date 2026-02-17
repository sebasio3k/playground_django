from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('minilibrary', views.index, name='minilibrary'),
    path('recomendar/<int:book_id>', views.add_review, name='recommend_book'),
    path('recomendarForm/<int:book_id>', views.add_review_form, name='recommend_book_form'),
    path('hello-fbv', views.hello, name='hello-fbv'),
    path('hello-cbv', views.Hello.as_view(), name='hello-cbv'),
    path('', views.WelcomeView.as_view(), name='welcome'),
    path('books', views.BookListView.as_view(), name='book-list'),
    path('books/add', views.add_book, name='add-book'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('book/<int:pk>/review', views.ReviewCreateView.as_view(), name='create-review'),
    path('book/<int:book_id>/review-update/<int:pk>', views.ReviewUpdateView.as_view(), name='update-review'),
    path('book/<int:book_id>/review-delete/<int:pk>', views.ReviewDeleteView.as_view(), name='delete-review'),
    path('home-middle', views.Home, name='home'),
    path('counter/', views.visit_counter, name='counter'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
