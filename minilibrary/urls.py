from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='minilibrary'),
    path('recomendar/<int:book_id>', views.add_review, name='recommend_book'),
    path('recomendarForm/<int:book_id>', views.add_review_form, name='recommend_book_form')
]
