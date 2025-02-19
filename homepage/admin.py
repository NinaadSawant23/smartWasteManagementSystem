from django.contrib import admin
from .models import Subscriber

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'email', 'phone', 'created_at')
#     view_qr_codes.allow_tags = True
#     view_qr_codes.short_description = 'QR Codes'

    search_fields = ('fname', 'lname', 'email')