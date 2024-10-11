from django.contrib import admin
from django import forms
from .models import Pattern, Category, GalleryImage
import json

class PatternAdminForm(forms.ModelForm):
    class Meta:
        model = Pattern
        fields = '__all__'

    def clean_instructions(self):
        instructions = self.cleaned_data['instructions']
        # Ensure instructions is a valid JSON array
        if isinstance(instructions, str):
            try:
                instructions = json.loads(instructions)
            except json.JSONDecodeError:
                raise forms.ValidationError("Instructions must be a valid JSON array.")
        return instructions


class PatternAdmin(admin.ModelAdmin):
    form = PatternAdminForm

admin.site.register(Category)
admin.site.register(GalleryImage)
admin.site.register(Pattern, PatternAdmin)