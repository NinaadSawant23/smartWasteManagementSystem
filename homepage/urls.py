from django.urls import path
from homepage import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path("", views.home, name='homepage'),
    path("loginhome",views.loginhome, name='loginhome'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('works/', views.register, name='works'),
    path('who/', views.who, name='who'),
    path('schedule/', views.schedule, name='schedule'),
    path('contact/', views.contact_view, name='contact'),
    path('schedule/', views.register, name='schedule'),
    path('pickuphistory/', views.pickuphistory, name='pickuphistory'),
    path('profile/', views.profile, name='profile'),
    path('contact/success/', views.contact_success_view, name='contact_success'),
    path('request-pickup/', views.request_pickup, name='request_pickup'),
    path('logout/', LogoutView.as_view(next_page='homepage'), name='logout'),
    ]