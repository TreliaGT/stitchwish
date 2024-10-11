from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# Create your models here.
class Pattern(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    feature_image = models.ImageField(upload_to='patterns/images/')
    instructions = models.JSONField()
    categories = models.ManyToManyField(Category, related_name='patterns')  # Use ManyToManyField for multiple categories
    time_to_make = models.CharField(max_length=100)  # e.g., "2 hours"
    material_list = models.TextField()
    is_paid = models.BooleanField(default=False)
    website_link = models.URLField(blank=True, null=True)
    youtube_link = models.URLField(blank=True, null=True)
    PDF_link = models.URLField(blank=True, null=True)
    pdf_file = models.FileField(upload_to='patterns/pdfs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class GalleryImage(models.Model):
    pattern = models.ForeignKey('Pattern', related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='patterns/gallery/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.caption or "Gallery Image"
    

class PatternUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.pattern.title}"
    