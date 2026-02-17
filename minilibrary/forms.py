from django import forms
from .models import Review, Book

BAD_WORDS = ['malo', 'mugroso', 'estupido', 'wey', 'perro', 'mierda']

class ReviewSimpleForm(forms.Form):
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Califica de (1-5)',
            'class': 'form-control',
        })
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Escribe tu comentario',
            'class': 'form-control',
            'rows': 4
        })
    )
    

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        exclude = ['user', 'book']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'placeholder': 'Califica de (1-5)',
                'class': 'form-control',
                'min': 1,
                'max': 5
            }),
            'text': forms.Textarea(attrs={
                'placeholder': 'Escribe tu comentario',
                'class': 'form-control',
                'rows': 4
            }),
        }
        
    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 5:
            raise forms.ValidationError("La calificación debe estar entre 1 y 5.")
        return rating
    
    def clean(self):
        cleaned_data = super().clean()
        rating = cleaned_data.get('rating')
        text = cleaned_data.get('text') or ''
        
        if rating == 1 and len(text) < 10:
            raise forms.ValidationError("Si la calificación es de 1 estrella, por favor explica mejor tu opinión.")
        
        return cleaned_data
    
    def clean_text(self):
        text = self.cleaned_data['text']
        for word in BAD_WORDS:
            if word in text.lower():
                raise forms.ValidationError(f"El comentario contiene una palabra prohibida: {word}")
        return text
        
        

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genres', 'publication_date', 'isbn', 'pages', 'cover']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'genres': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'publication_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'pages': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'cover': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
    def clean_cover(self):
        cover = self.cleaned_data['cover']
        max_size = 2 * 1024 * 1024
        if cover:
            if cover.size > max_size:
                raise forms.ValidationError("El archivo de la portada debe ser menor de 2MB.")
            
        if cover.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
            raise forms.ValidationError("El archivo de la portada debe ser una imagen.")
        
        return cover
    
    def clean_pages(self):
        pages = self.cleaned_data['pages']
        if pages < 1:
            raise forms.ValidationError("El libro debe tener al menos 1 página.")
        return pages