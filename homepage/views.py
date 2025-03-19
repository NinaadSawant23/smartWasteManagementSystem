from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "home.html", {})


@login_required
def loginhome(request):
    return render(request, "loginhome.html", {})


def register(request):
    return render(request, "home.html", {})


def custom_login(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('loginhome')  # Redirect all users to profile page

        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')

    return render(request, 'login.html', {'form': form})
