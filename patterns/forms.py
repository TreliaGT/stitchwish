from django import forms
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

class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['image', 'caption']
