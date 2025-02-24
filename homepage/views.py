from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "home.html", {})
def register(request):
    return render(request, "home.html", {})

def custom_login(request):
    return render(request, "home.html", {})