from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='minilibrary'),
    path('recomendar/<int:book_id>', views.add_review, name='recommend_book'),
    path('recomendarForm/<int:book_id>', views.add_review_form, name='recommend_book_form'),
    path('hello-fbv', views.hello, name='hello-fbv'),
    path('hello-cbv', views.Hello.as_view(), name='hello-cbv'),
    path('welcome', views.WelcomeView.as_view(), name='welcome'),
    path('books', views.BookListView.as_view(), name='book-list'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('book/<int:pk>/review', views.ReviewCreateView.as_view(), name='create-review'),
    path('book/<int:book_id>/review-update/<int:pk>', views.ReviewUpdateView.as_view(), name='update-review'),
]
