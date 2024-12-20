from django.shortcuts import render, redirect, get_object_or_404
from .models import Pattern ,Category , PatternUser , GalleryImage
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import PatternForm, GalleryImageFormSet , SearchForm
from django.contrib import messages
from django.core.files.storage import default_storage 
import json 

@login_required
def pattern_list(request):
    form = SearchForm()
    patterns = Pattern.objects.all()
    paginator = Paginator(patterns, 12) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    liked_patterns = PatternUser.objects.filter(user=request.user).values_list('pattern_id', flat=True)
    print(f"Categories: {categories}")
    return render(request, 'pattern_list.html', {'patterns': page_obj , 'categories' : categories , 'title' : "Patterns Listing" ,  'liked_patterns': liked_patterns , 'form': form})


@login_required
def category_patterns(request, category_id):
    category = get_object_or_404(Category, id=category_id)  # Get the category by ID
    patterns = category.patterns.all()  # Retrieve all patterns associated with this category
    categories = Category.objects.all()
    paginator = Paginator(patterns, 12) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    liked_patterns = PatternUser.objects.filter(user=request.user).values_list('pattern_id', flat=True)
    return render(request, 'pattern_list.html', {'category': category, 'patterns': page_obj , 'categories' : categories , 'title' : category.name ,  'liked_patterns': liked_patterns})

@login_required
def pattern_detail(request, pk):
    pattern = Pattern.objects.get(pk=pk)
    try:
        instructions = json.loads(pattern.instructions)
    except json.JSONDecodeError:
        instructions = []  # In case of invalid JSON, default to an empty list
    return render(request, 'pattern_detail.html', {'pattern': pattern , 'instructions': instructions})

@login_required
def liked(request):
    wishlist_entries = PatternUser.objects.filter(user=request.user)
    patterns = [entry.pattern for entry in wishlist_entries]
    liked_patterns = PatternUser.objects.filter(user=request.user).values_list('pattern_id', flat=True)
    paginator = Paginator(patterns, 12) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pattern_list.html', {'patterns': page_obj ,  'title' : "My Liked List" ,  'liked_patterns': liked_patterns})

@login_required
def my_pattern_list(request):
    patterns = Pattern.objects.filter(user=request.user)  # Only get patterns for the logged-in user
    paginator = Paginator(patterns, 12) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pattern_list.html', {'patterns': page_obj, 'title' : "My Patterns"})

@login_required
def search(request):
    form = SearchForm()
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Pattern.objects.filter(title__icontains=query)  # Search in titles
            # You can also search in descriptions or other fields
            # results = Pattern.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'pattern_list.html', {'form': form, 'patterns': results})

@login_required
def add_to_wishlist(request, pattern_id):
    pattern = get_object_or_404(Pattern, id=pattern_id)
    # Create or get the PatternUser instance
    pattern_user, created = PatternUser.objects.get_or_create(user=request.user, pattern=pattern)
    return redirect('pattern_list')  # Redirect to the pattern list or wishlist page

@login_required
def remove_from_wishlist(request, pattern_id):
    pattern = get_object_or_404(Pattern, id=pattern_id)
    
    # Attempt to retrieve the PatternUser instance associated with the user and the pattern
    try:
        pattern_user = PatternUser.objects.get(user=request.user, pattern=pattern)
        pattern_user.delete()  # Delete the instance to remove from wishlist
    except PatternUser.DoesNotExist:
        pass

    return redirect('pattern_list')  # Redirect to the pattern list or wishlist page

@login_required
def create_pattern(request):
    if request.method == "POST":
        form = PatternForm(request.POST, request.FILES)
        formset = GalleryImageFormSet(request.POST, request.FILES, queryset=GalleryImage.objects.none())
        if form.is_valid() and formset.is_valid():
            # Convert instructions to JSON format
            pattern = form.save(commit=False)
            pattern.user = request.user
            
            # Split the instructions by newlines and filter out empty lines
            instructions_text = form.cleaned_data['instructions']
            instructions_list = [step.strip() for step in instructions_text.splitlines() if step.strip()]
            pattern.instructions =  json.dumps(instructions_list)  # Store as a list

            pattern.save()
            form.save_m2m()
            
            # Save gallery images
            for gallery_image_form in formset:
                if gallery_image_form.cleaned_data and not gallery_image_form.cleaned_data.get('DELETE', False):
                    if gallery_image_form.cleaned_data['image']:
                        GalleryImage.objects.create(pattern=pattern, **gallery_image_form.cleaned_data)

            messages.success(request, 'Pattern created successfully!')
            return redirect('pattern_list')
        else:
            # Error handling
            error_messages = []
            for field in form:
                for error in field.errors:
                    error_messages.append(f"{field.label}: {error}")
            for error in form.non_field_errors():
                error_messages.append(error)
            for gallery_image_form in formset:
                for error in gallery_image_form.non_field_errors():
                    error_messages.append(error)
                for field in gallery_image_form:
                    for error in field.errors:
                        error_messages.append(f"{field.label}: {error}")

            error_message = "Please correct the following errors:<br>" + "<br>".join(error_messages)
            messages.error(request, error_message)
    else:
        form = PatternForm()
        formset = GalleryImageFormSet(queryset=GalleryImage.objects.none())

    return render(request, 'create_pattern.html', {'form': form, 'formset': formset})


@login_required
def update_pattern(request, pattern_id):
    pattern = get_object_or_404(Pattern, id=pattern_id, user=request.user)
    
    if request.method == "POST":
        form = PatternForm(request.POST, request.FILES, instance=pattern)
        
        # Pass the existing gallery images to the formset
        formset = GalleryImageFormSet(request.POST, request.FILES, queryset=GalleryImage.objects.filter(pattern=pattern))
        
        if form.is_valid() and formset.is_valid():
            # Save the updated pattern
            pattern.save()

            # Handle the gallery images
            for gallery_image_form in formset:
                # If the DELETE checkbox is checked, delete the image
                if gallery_image_form.cleaned_data.get('DELETE'):
                    gallery_image_form.instance.delete()
                elif gallery_image_form.cleaned_data.get('image'):
                    # Save the gallery image, which includes the id field
                    gallery_image_form.save()

            messages.success(request, 'Pattern updated successfully!')
            return redirect('pattern_list')
    else:
        form = PatternForm(instance=pattern)
        formset = GalleryImageFormSet(queryset=GalleryImage.objects.filter(pattern=pattern))

    return render(request, 'update_pattern.html', {'form': form, 'formset': formset})






@login_required
def delete_pattern(request, pattern_id):
    pattern = get_object_or_404(Pattern, id=pattern_id, user=request.user)  # Ensure the user owns the pattern
    if request.method == "POST":
        # Delete the feature image if it exists
        if pattern.feature_image:  # Ensure feature_image exists
            default_storage.delete(pattern.feature_image.name)  # Delete the feature image file

        # Delete the PDF file if it exists
        if pattern.pdf_file:  # Ensure pdf_file exists
            default_storage.delete(pattern.pdf_file.name)  # Delete the PDF file

        # Delete associated gallery images if any
        gallery_images = GalleryImage.objects.filter(pattern=pattern)  # Get associated gallery images
        for image in gallery_images:
            if image.image:  # Assuming 'image' is the field name for the image in the GalleryImage model
                default_storage.delete(image.image.name)  # Delete the gallery image file
            image.delete()  # Delete the gallery image instance

        pattern.delete()  # Delete the pattern
        return redirect('pattern_list')  # Redirect to the pattern list page

    return render(request, 'delete_pattern.html', {'pattern': pattern})