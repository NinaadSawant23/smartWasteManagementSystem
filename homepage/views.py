from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
from homepage.forms import UserRegistrationForm
from .models import ContactSubmission


def home(request):
    return render(request, "home.html", {})


@login_required
def loginhome(request):
    return render(request, "loginhome.html", {})


def register(request):
    role = request.POST.get('role', None)
    subscriber_form = UserRegistrationForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if role == 'Subscriber' and subscriber_form.is_valid():
            subscriber_form.save()
            messages.success(request, "Subscriber account created successfully!")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")

    return render(request, 'register.html', {
        'subscriber_form': subscriber_form
    })

def who(request):
    return render(request, 'who.html')

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


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactSubmission.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            return redirect('contact_success')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})