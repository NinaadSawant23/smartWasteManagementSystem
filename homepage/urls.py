from django.urls import path
from homepage import views
from django.contrib.auth.views import LogoutView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name='homepage'),
    path("loginhome",views.loginhome, name='loginhome'),
    path('register/', views.register, name='register'),
    path('services/', views.services, name='services'),
    path('login/', views.custom_login, name='login'),
    path('works/', views.works, name='works'),
    path('who/', views.who, name='who'),
    path('schedule/', views.schedule, name='schedule'),
    path('contact/', views.contact_view, name='contact'),
    path('schedule/', views.register, name='schedule'),
    path('pickuphistory/', views.pickuphistory, name='pickuphistory'),
    path('profile/', views.profile, name='profile'),
    path('contact/success/', views.contact_success_view, name='contact_success'),
    path('request-pickup/', views.request_pickup, name='request_pickup'),
    path('logout/', LogoutView.as_view(next_page='homepage'), name='logout'),
    path('driver_dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('worker_dashboard/', views.worker_dashboard, name='worker_dashboard'),
    path('settings/', views.settings, name='settings'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)