from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import PickupRequest, QRCode, Subscriber

@receiver(pre_save, sender=PickupRequest)
def detect_status_change(sender, instance, **kwargs):
    if instance.pk:
        existing_request = PickupRequest.objects.get(pk=instance.pk)
        instance._previous_status = existing_request.status




@receiver(post_save, sender=Subscriber)
def generate_qr_codes(sender, instance, created, **kwargs):
    if created:
        QRCode.objects.create(subscriber=instance)
