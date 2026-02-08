from django import forms


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
