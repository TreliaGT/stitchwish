from django.shortcuts import render, redirect, get_object_or_404
from .models import Pattern ,Category , PatternUser
from django.contrib.auth.decorators import login_required
from .forms import PatternForm, GalleryImageForm

@login_required
def pattern_list(request):
    patterns = Pattern.objects.all()
    categories = Category.objects.all()
    return render(request, 'pattern_list.html', {'patterns': patterns , 'categories' : categories , 'title' : "Patterns Listing"})
@login_required

def category_patterns(request, category_id):
    category = get_object_or_404(Category, id=category_id)  # Get the category by ID
    patterns = category.patterns.all()  # Retrieve all patterns associated with this category
    categories = Category.objects.all()
    return render(request, 'pattern_list.html', {'category': category, 'patterns': patterns , 'categories' : categories})

@login_required
def pattern_detail(request, pk):
    pattern = Pattern.objects.get(pk=pk)
    return render(request, 'pattern_detail.html', {'pattern': pattern})

@login_required
def liked(request):
    patterns = Pattern.objects.filter(user=request.user)  # Get patterns associated with the logged-in user
    categories = Category.objects.all()
    return render(request, 'pattern_list.html', {'patterns': patterns , 'categories' : categories, 'title' : "My Liked List"})

@login_required
def pattern_list(request):
    patterns = Pattern.objects.filter(user=request.user)  # Only get patterns for the logged-in user
    return render(request, 'pattern_list.html', {'patterns': patterns, 'title' : "My Patterns"})


@login_required
def add_to_wishlist(request, pattern_id):
    pattern = get_object_or_404(Pattern, id=pattern_id)
    # Create or get the PatternUser instance
    pattern_user, created = PatternUser.objects.get_or_create(user=request.user, pattern=pattern)
    return redirect('pattern_list')  # Redirect to the pattern list or wishlist page


@login_required
def wishlist(request):
    wishlist_items = PatternUser.objects.filter(user=request.user)
    return render(request, 'pattern_list.html', {'patterns': wishlist_items})

@login_required
def create_pattern(request):
    if request.method == "POST":
        form = PatternForm(request.POST, request.FILES)
        if form.is_valid():
            pattern = form.save(commit=False)
            pattern.user = request.user  # Associate the pattern with the logged-in user
            pattern.save()  # Save the pattern to the database
            return redirect('pattern_list')  # Redirect to the pattern list page
    else:
        form = PatternForm()
    return render(request, 'create_pattern.html', {'form': form})


@login_required
def update_pattern(request, pattern_id):
    pattern = get_object_or_404(Pattern, id=pattern_id, user=request.user)  # Ensure the user owns the pattern
    if request.method == "POST":
        form = PatternForm(request.POST, request.FILES, instance=pattern)
        if form.is_valid():
            form.save()  # Update the pattern
            return redirect('pattern_list')  # Redirect to the pattern list page
    else:
        form = PatternForm(instance=pattern)
    return render(request, 'patterns/update_pattern.html', {'form': form})

@login_required
def delete_pattern(request, pattern_id):
    pattern = get_object_or_404(Pattern, id=pattern_id, user=request.user)  # Ensure the user owns the pattern
    if request.method == "POST":
        pattern.delete()  # Delete the pattern
        return redirect('pattern_list')  # Redirect to the pattern list page
    return render(request, 'patterns/delete_pattern.html', {'pattern': pattern})