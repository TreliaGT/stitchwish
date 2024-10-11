from django.urls import path
from .views import pattern_list, pattern_detail , projects, wishlist

urlpatterns = [
    path('patterns/', pattern_list, name='pattern_list'),
    path('patterns/<int:pk>/', pattern_detail, name='pattern_detail'),
    path('projects/', projects, name='projects'),
    path('wistlist/', wishlist, name='wishlist'),
]
