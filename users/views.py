# users/views.py
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import login

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Create user but don't save password yet
            user.set_password(form.cleaned_data['password'])  # Encrypt password
            user.save()
            login(request, user)  # Log in the user automatically after registration
            return redirect('home')  # Redirect to homepage or any other page
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})