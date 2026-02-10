from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='minilibrary'),
    path('recomendar/<int:book_id>', views.add_review, name='recommend_book'),
    path('recomendarForm/<int:book_id>', views.add_review_form, name='recommend_book_form'),
    path('hello-fbv', views.hello, name='hello-fbv'),
    path('hello-cbv', views.Hello.as_view(), name='hello-cbv'),
]
