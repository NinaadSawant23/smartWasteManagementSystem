from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, "home.html", {})

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.save()  
            login(request, user) 
            messages.success(request, "Registration successful. Welcome!")
            return redirect('homepage')  
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")

    return render(request, 'register.html', {'form': form})

def custom_login(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect('homepage')  # Redirect all users to profile page

        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')

    return render(request, 'login.html', {'form': form})