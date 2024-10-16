from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Log the user in immediately after registration
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('pattern_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('pattern_list')  # Change this to your home view
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request , 'login.html')

def profile_view(request):
    return render(request, 'profile.html')
