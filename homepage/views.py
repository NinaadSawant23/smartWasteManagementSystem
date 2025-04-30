import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.db import models
from .forms import ContactForm, PickupRequestForm, DriverRegistrationForm, RedemptionWorkerRegistrationForm
from homepage.forms import UserRegistrationForm
from .models import ContactSubmission, Subscriber, AccountBalance, PickupRequest, RecyclingHistory
from django.db.models import Sum


def home(request):
    return render(request, "home.html", {})


@login_required
def loginhome(request):
    return render(request, "loginhome.html", {})


def register(request):
    role = request.POST.get('role', None)
    subscriber_form = UserRegistrationForm(request.POST or None, request.FILES or None)
    driver_form = DriverRegistrationForm(request.POST or None)
    worker_form = RedemptionWorkerRegistrationForm(request.POST or None)

    if request.method == 'POST':
        if role == 'Subscriber' and subscriber_form.is_valid():
            subscriber_form.save()
            messages.success(request, "Subscriber account created successfully!")
            return redirect('login')

        elif role == 'Driver' and driver_form.is_valid():
            driver_form.save()
            messages.success(request, "Driver account created successfully!")
            return redirect('login')

        elif role == 'RedemptionCenterWorker' and worker_form.is_valid():
            worker_form.save()
            messages.success(request, "Redemption Center Worker account created successfully!")
            return redirect('login')

        else:
            messages.error(request, "Please correct the errors below.")

    return render(request, 'register.html', {
        'subscriber_form': subscriber_form,
        'driver_form': driver_form,
        'worker_form': worker_form,
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
            if hasattr(user, 'driver_profile'):
                login(request, user)
                return redirect('driver_dashboard')

            elif hasattr(user, 'worker_profile'):
                login(request, user)
                return redirect('worker_dashboard')

            else:
                login(request, user)
                return redirect('profile')

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

@login_required
def driver_dashboard(request):
    if not hasattr(request.user, 'driver_profile'):
        messages.error(request, "Access denied.")
        return redirect('login')

    driver = request.user.driver_profile

    # 🛠️  Only fetch pickup requests assigned to this driver!
    pickup_requests = PickupRequest.objects.filter(status='Accepted', driver=driver)

    scanned_bag_count = 0
    num_bags = 0
    selected_pickup_request = None

    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get("action")
        pickup_request_id = data.get("pickup_request_id")

        try:
            pickup_request = PickupRequest.objects.get(pk=pickup_request_id, driver=driver)

            if action == "add_bag":
                if pickup_request.scanned_bag_count < pickup_request.num_bags:
                    pickup_request.scanned_bag_count += 1
                    pickup_request.save()
                    return JsonResponse({"success": True, "message": f"Bag {pickup_request.scanned_bag_count} added!"})
                else:
                    return JsonResponse({"success": False, "message": "All bags already scanned!"})

            elif action == "mark_picked_up":
                if pickup_request.scanned_bag_count == pickup_request.num_bags:
                    pickup_request.status = "Picked Up"
                    pickup_request.save()
                    return JsonResponse({"success": True, "message": "Pickup request marked as Picked Up!"})
                else:
                    return JsonResponse({"success": False, "message": "Not all bags have been scanned!"})

        except PickupRequest.DoesNotExist:
            return JsonResponse({"success": False, "message": "Invalid or Unauthorized Pickup Request!"})

    pickup_request_id = request.GET.get("pickup_request_id")
    if pickup_request_id:
        try:
            selected_pickup_request = PickupRequest.objects.get(pk=pickup_request_id, driver=driver)
            scanned_bag_count = selected_pickup_request.scanned_bag_count
            num_bags = selected_pickup_request.num_bags
        except PickupRequest.DoesNotExist:
            selected_pickup_request = None

    context = {
        "driver": driver,
        "pickup_requests": pickup_requests,
        "scanned_bag_count": scanned_bag_count,
        "num_bags": num_bags,
        "selected_pickup_request": selected_pickup_request,
    }
    return render(request, "driver_dashboard.html", context)

@login_required
def worker_dashboard(request):
    if not hasattr(request.user, 'worker_profile'):
        messages.error(request, "Access denied.")
        return redirect('login')

    worker = request.user.worker_profile
    scanned_bags = request.session.get('scanned_bags', [])
    total_points = request.session.get('total_points', 0)
    pickup_request = None

    if request.method == "POST":
        bag_id = request.POST.get("bag_id")
        action = request.POST.get("action")
        num_items = request.POST.get("num_items")  # Get the number of items from the form

        print(f"INFO: Action received: {action}")

        if action == "scan_bag":
            if not bag_id:
                print("ERROR: No Bag ID provided for scanning.")
                messages.error(request, "Please provide a valid Bag ID.")
                return redirect('worker_dashboard')

            if not num_items or int(num_items) < 1:
                print("ERROR: Invalid number of items.")
                messages.error(request, "Please provide a valid number of items.")
                return redirect('worker_dashboard')

            try:
                pickup_request = PickupRequest.objects.get(
                    user__subscriber_profile__qr_codes__id=bag_id,
                    status="Picked Up"
                )
                print(f"INFO: Pickup request found for Bag ID {bag_id}: {pickup_request}")
            except PickupRequest.DoesNotExist:
                print(f"ERROR: No active pickup request found for Bag ID {bag_id}.")
                messages.error(request, f"No active pickup request found for Bag ID {bag_id}.")
                return redirect('worker_dashboard')

            if len(scanned_bags) < pickup_request.num_bags:
                print(f"INFO: Scanning bag for pickup request: {pickup_request}")

                points = round(int(num_items) * 0.0322, 2)  # Calculate points based on the entered number of items

                scanned_bags.append({
                    "bag_id": bag_id,
                    "bag_number": len(scanned_bags) + 1,
                    "num_items": int(num_items),
                    "points": points,
                })
                total_points += points

                pickup_request.scanned_bag_count = len(scanned_bags)
                pickup_request._updated_by_worker = True
                pickup_request.save()

                request.session['scanned_bags'] = scanned_bags
                request.session['total_points'] = total_points

                print(f"INFO: Bag scanned successfully. Total scanned: {len(scanned_bags)}")
                messages.success(
                    request,
                    f"Bag {len(scanned_bags)} scanned: {num_items} items, {points} points.",
                )
            else:
                print("ERROR: All bags for this pickup request have already been scanned.")
                messages.error(request, "All bags for this pickup request have already been scanned.")

        elif action == "finalize":
            print("DEBUG: Finalize action triggered.")
            try:
                if scanned_bags:
                    bag_id = scanned_bags[0]["bag_id"]
                    pickup_request = PickupRequest.objects.get(
                        user__subscriber_profile__qr_codes__id=bag_id,
                        status="Picked Up"
                    )
                    print(f"INFO: Pickup request fetched for finalize: {pickup_request}")
                else:
                    raise ValueError("Scanned bags session is empty.")
            except PickupRequest.DoesNotExist:
                print(f"ERROR: No active pickup request found for Bag ID {bag_id}.")
                messages.error(request, "Failed to fetch the pickup request. Please try again.")
                return redirect('worker_dashboard')
            except Exception as e:
                print(f"ERROR: Unexpected error: {str(e)}")
                messages.error(request, "An unexpected error occurred.")
                return redirect('worker_dashboard')

            if len(scanned_bags) == pickup_request.num_bags:
                items_recycled = sum(bag['num_items'] for bag in scanned_bags)
                try:
                    RecyclingHistory.objects.create(
                        subscriber=pickup_request.user.subscriber_profile,
                        items_recycled=items_recycled,
                        points_earned=total_points,
                    )
                    print(f"INFO: Recycling history created for {pickup_request.user.subscriber_profile}")
                except Exception as e:
                    print(f"ERROR: Failed to create recycling history: {str(e)}")
                    messages.error(request, "Failed to save recycling history. Please try again.")
                    return redirect('worker_dashboard')

                pickup_request.status = "Completed"
                pickup_request.save()

                updated_pickup_request = PickupRequest.objects.get(pk=pickup_request.pk)
                if updated_pickup_request.status == "Completed":
                    print("INFO: Pickup request status successfully updated to 'Completed'.")
                    messages.success(
                        request,
                        "Pickup request finalized. Rewards have been added to the subscriber's account, and the status is updated to 'Completed'.",
                    )
                else:
                    print("ERROR: Pickup request status update failed.")
                    messages.error(
                        request,
                        "Pickup request could not be marked as 'Completed'. Please try again.",
                    )

                request.session.pop('scanned_bags', None)
                request.session.pop('total_points', None)

                return redirect('worker_dashboard')
            else:
                print(f"ERROR: Not all bags have been scanned. Scanned: {len(scanned_bags)}, Total: {pickup_request.num_bags}")
                messages.error(request, "Please scan all bags before finalizing.")

    return render(request, 'worker_dashboard.html', {
        'worker': worker,
        'pickup_request': pickup_request,
        'scanned_bags': scanned_bags,
        'total_points': total_points,
    })
