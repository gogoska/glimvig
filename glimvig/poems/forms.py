from django import forms
from .models import Rating, Poem

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value',]

class PoemForm(forms.ModelForm):
    class Meta:
        model = Poem
        fields = ['title', 'text', 'teaser',]