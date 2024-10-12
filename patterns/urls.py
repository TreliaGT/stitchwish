from django.urls import path
from .views import pattern_list, pattern_detail , liked ,pattern_list ,add_to_wishlist, category_patterns , create_pattern, update_pattern, delete_pattern, remove_from_wishlist,my_pattern_list

urlpatterns = [
    path('patterns/', pattern_list, name='pattern_list'),
    path('patterns/<int:pk>/', pattern_detail, name='pattern_detail'),
    path('liked/', liked, name='liked'),
    path('my_patterns/', my_pattern_list, name='my_patterns'),
    path('add_to_wishlist/<int:pattern_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:pattern_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('categories/<int:category_id>/', category_patterns, name='category_patterns'),
    path('patterns/create/', create_pattern, name='create_pattern'),
    path('patterns/update/<int:pattern_id>/', update_pattern, name='update_pattern'),
    path('patterns/delete/<int:pattern_id>/', delete_pattern, name='delete_pattern'),
]
