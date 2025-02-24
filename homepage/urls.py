from django.urls import path
from homepage import views

urlpatterns = [
    path("", views.home, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('works/', views.register, name='works'),
    path('schedule/', views.register, name='schedule'),
    ]