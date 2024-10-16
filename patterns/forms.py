from django import forms
from django.forms import modelformset_factory
from .models import Pattern, GalleryImage

class PatternForm(forms.ModelForm):
    class Meta:
        model = Pattern
        fields = [
            'title',
            'feature_image',
            'instructions',
            'categories',
            'time_to_make',
            'material_list',
            'is_paid',
            'website_link',
            'youtube_link',
            'pdf_file',
            'pdf_link'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'feature_image': forms.FileInput(attrs={'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter each instruction on a new line'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),  # Multiple select for categories
            'time_to_make': forms.TextInput(attrs={'class': 'form-control'}),
            'material_list': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'website_link': forms.URLInput(attrs={'class': 'form-control'}),
            'youtube_link': forms.URLInput(attrs={'class': 'form-control'}),
            'pdf_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pdf_link': forms.URLInput(attrs={'class': 'form-control'}),
        }

# Create a formset for GalleryImage
GalleryImageFormSet = modelformset_factory(GalleryImage, fields=('image', 'caption'), extra=6)



class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)