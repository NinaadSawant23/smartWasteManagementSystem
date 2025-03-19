from django.urls import path
from homepage import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path("", views.home, name='homepage'),
    path("loginhome",views.loginhome, name='loginhome'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('works/', views.register, name='works'),
    path('schedule/', views.register, name='schedule'),
    path('logout/', LogoutView.as_view(next_page='homepage'), name='logout'),
    ]