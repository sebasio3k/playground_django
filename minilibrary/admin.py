from datetime import datetime
from django.contrib import admin
from .models import Author, Genre, Book, BookDetail, Review, Loan, Recommendation
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()

# Register your models here.

# ACTIONS
@admin.action(description="Marcar prestamos como devueltos")
def mark_as_returned(modeladmin, request, queryset):
    queryset.update(is_returned=True, return_date=datetime.now())

# INLIES
class LoanInline(admin.TabularInline):
    model = Loan
    extra = 1

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    
class BookDetailInline(admin.TabularInline):
    model = BookDetail
    can_delete = False
    verbose_name_plural = 'Detalles del libro'
    
class CustomUserAdmin(BaseUserAdmin):
    inlines = [LoanInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')

# MODELS REGISTERS
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = [ReviewInline, BookDetailInline]
    list_display = ('title', 'author', 'pages', 'publication_date' )
    search_fields = ('title', 'author__name')
    list_filter = ('author', 'genres')
    ordering = ['-publication_date']
    date_hierarchy = 'publication_date'
    readonly_fields = ('pages',)
    autocomplete_fields = ('author', 'genres',)
    
    fieldsets = (
        ("Información General", {
            "fields": (
                "title", "author", "genres", "publication_date",
            ),
        }),
        ("Detalles", {
            "fields": (
                "isbn", "pages",
            ),
            "classes": ("collapse",),
        }),
    )
    
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    readonly_fields = ('loan_date',)
    list_display = ('user', 'book', 'loan_date', 'return_date', 'is_returned')
    actions = [mark_as_returned]
    raw_id_fields = ('user', 'book')
    
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date',)
    search_fields = ('name',)
    
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# admin.site.register(Author)
# admin.site.register(Genre)
# admin.site.register(Book, BookAdmin)
admin.site.register(BookDetail)
admin.site.register(Review)
# admin.site.register(Loan, LoanAdmin)
admin.site.register(Recommendation)


# UNREGISTER USER ADMIN AND RE-REGISTER CustomUserAdmin
try:
    admin.site.unregister(User)
except (admin.sites.NotRegistered, admin.sites.AlreadyRegistered):
    pass

admin.site.register(User, CustomUserAdmin)