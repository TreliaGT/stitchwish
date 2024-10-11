from django.shortcuts import render, redirect, get_object_or_404
from .models import Pattern ,Category , PatternUser , GalleryImage
from django.contrib.auth.decorators import login_required
from .forms import PatternForm, GalleryImageFormSet
from django.contrib import messages
from django.core.files.storage import default_storage 
import json 

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
    try:
        instructions = json.loads(pattern.instructions)
    except json.JSONDecodeError:
        instructions = []  # In case of invalid JSON, default to an empty list
    return render(request, 'pattern_detail.html', {'pattern': pattern , 'instructions': instructions})

@login_required
def liked(request):
    wishlist_entries = PatternUser.objects.filter(user=request.user)
    patterns = [entry.pattern for entry in wishlist_entries]
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
            for gallery_image in formset:
                if gallery_image.cleaned_data and gallery_image.cleaned_data['image']:
                    GalleryImage.objects.create(pattern=pattern, **gallery_image.cleaned_data)

            messages.success(request, 'Pattern created successfully!')
            return redirect('pattern_list')
        else:
            error_messages = []
            for field in form:
                for error in field.errors:
                    error_messages.append(f"{field.label}: {error}")
            for error in form.non_field_errors():
                error_messages.append(error)
            # Add formset errors
            for gallery_image_form in formset:
                for error in gallery_image_form.non_field_errors():
                    error_messages.append(error)
                for field in gallery_image_form:
                    for error in field.errors:
                        error_messages.append(f"{field.label}: {error}")

            # Join all errors into a single message
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
        formset = GalleryImageFormSet(request.POST, request.FILES, queryset=pattern.galleryimage_set.all())
        if form.is_valid() and formset.is_valid():
            # Convert instructions to JSON format
            pattern = form.save(commit=False)
            pattern.user = request.user
            
            # Split the instructions by newlines and filter out empty lines
            instructions_text = form.cleaned_data['instructions']
            instructions_list = [step.strip() for step in instructions_text.splitlines() if step.strip()]
            pattern.instructions = json.dumps(instructions_list)  # Store as a list

            pattern.save()
                
            # Save categories (Many-to-Many relationship)
            form.save_m2m()  # Save the categories
                
            # Save new gallery images
            try:
                for gallery_image in formset:
                    if gallery_image.cleaned_data and gallery_image.cleaned_data['image']:
                        GalleryImage.objects.create(pattern=pattern, **gallery_image.cleaned_data)
            except:
                pass
            messages.success(request, 'Pattern updated successfully!')
            return redirect('pattern_list')

        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PatternForm(instance=pattern)
        try:
            formset = GalleryImageFormSet(queryset=pattern.gallery_images.all())  # Populate formset with existing images
        except:
            formset = GalleryImageFormSet(queryset=GalleryImage.objects.none())  
    return render(request, 'update_pattern.html', {'form': form, 'formset': formset})

@login_required
def delete_pattern(request, pattern_id):
    pattern = get_object_or_404(Pattern, id=pattern_id, user=request.user)  # Ensure the user owns the pattern
    if request.method == "POST":
        # Delete associated gallery images if any
        if pattern.feature_image:
            default_storage.delete(pattern.feature_image) 

        # Delete the PDF file if it exists
        if pattern.pdf_file:
            default_storage.delete(pattern.pdf_file)  # Delete the PDF file

        gallery_images = GalleryImage.objects.filter(pattern=pattern)  # Get associated gallery images
        for image in gallery_images:
            if image.image:  # Assuming 'image' is the field name for the image in the GalleryImage model
                default_storage.delete(image.image.name)  # Delete the gallery image file
            image.delete()  # Delete the gallery image instance

        pattern.delete()  # Delete the pattern
        return redirect('pattern_list')  # Redirect to the pattern list page
    return render(request, 'delete_pattern.html', {'pattern': pattern})