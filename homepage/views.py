from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.db import models
from .forms import ContactForm, PickupRequestForm
from homepage.forms import UserRegistrationForm
from .models import ContactSubmission, Subscriber, AccountBalance, PickupRequest
from django.db.models import Sum


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


def contact_success_view(request):
    return render(request, 'contact_success.html')

@login_required
def request_pickup(request):
    user = request.user
    pickup_request = PickupRequest.objects.filter(user=user).order_by('-created_at').first()

    if pickup_request and pickup_request.status != "Completed":
        return render(request, 'request.html', {
            'pickup_request': pickup_request,
            'form': None,
            'error_message': "You cannot submit a new pickup request until your current request is completed.",
        })

    if request.method == "POST":
        form = PickupRequestForm(request.POST)
        if form.is_valid():
            ready_for_pickup = form.cleaned_data['ready_for_pickup']
            num_bags = form.cleaned_data['num_bags']

            PickupRequest.objects.create(
                user=user,
                ready_for_pickup=ready_for_pickup,
                num_bags=num_bags,
                status="Pending"
            )
            messages.success(request, "Your pickup request has been submitted successfully!")
            return redirect('request_pickup')

    form = PickupRequestForm()
    return render(request, 'request.html', {
        'pickup_request': pickup_request,
        'form': form,
    })

@login_required
def schedule(request):
    return render(request, 'schedule.html')


def pickuphistory(request):
    return render(request, 'pickuphistory.html')


@login_required
def profile(request):
    subscriber = get_object_or_404(Subscriber, account_id=request.user.id)

    subscriber.refresh_from_db()

    total_points = subscriber.recycling_history.aggregate(
        total_points=Sum('points_earned')
    )['total_points'] or 0

    if hasattr(subscriber, 'account_balance'):
        subscriber.account_balance.balance = round(total_points, 2)
        subscriber.account_balance.save()
    else:
        subscriber.account_balance = AccountBalance.objects.create(
            subscriber=subscriber, balance=round(total_points, 2)
        )

    return render(request, 'profile.html', {'subscriber': subscriber})

