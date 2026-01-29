from django.contrib import admin
from .models import Author, Genre, Book, BookDetail, Review, Loan, Recommendation

# Register your models here.

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    
class BookDetailInline(admin.TabularInline):
    model = BookDetail
    can_delete = False
    verbose_name_plural = 'Detalles del libro'
    
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = [ReviewInline, BookDetailInline]
    list_display = ('title', 'author', 'pages', 'publication_date' )
    search_fields = ('title', 'author__name')
    list_filter = ('author', 'genres')
    ordering = ['-publication_date']
    date_hierarchy = 'publication_date'


admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(Book, BookAdmin)
admin.site.register(BookDetail)
admin.site.register(Review)
admin.site.register(Loan)
admin.site.register(Recommendation)
