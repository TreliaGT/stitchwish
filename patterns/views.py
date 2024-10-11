from django.shortcuts import render
from .models import Pattern ,Category
from django.contrib.auth.decorators import login_required

@login_required
def pattern_list(request):
    patterns = Pattern.objects.all()
    categories = Category.objects.all()
    return render(request, '/pattern_list.html', {'patterns': patterns , 'categories' : categories , 'title' : "Patterns Listing"})

@login_required
def pattern_detail(request, pk):
    pattern = Pattern.objects.get(pk=pk)
    return render(request, '/pattern_detail.html', {'pattern': pattern})

@login_required
def projects(request):
    patterns = Pattern.objects.filter(user=request.user , is_project=True)  # Get patterns associated with the logged-in user
    categories = Category.objects.all()
    return render(request, '/pattern_list.html', {'patterns': patterns , 'categories' : categories, 'title' : "My Projects"})

@login_required
def wishlist(request):
    patterns = Pattern.objects.filter(user=request.user , is_wishlist =True)  # Get patterns associated with the logged-in user
    categories = Category.objects.all()
    return render(request, '/pattern_list.html', {'patterns': patterns , 'categories' : categories , 'title' : "My Wishlist"})