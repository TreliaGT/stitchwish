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
        ]

# Create a formset for GalleryImage
GalleryImageFormSet = modelformset_factory(GalleryImage, fields=('image', 'caption'), extra=6)
