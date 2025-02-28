# Generated by Django 5.1.6 on 2025-02-19 03:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Subscriber",
            fields=[
                ("account_id", models.AutoField(primary_key=True, serialize=False)),
                ("fname", models.CharField(max_length=100)),
                ("lname", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone", models.CharField(max_length=15)),
                ("street_address", models.CharField(default="", max_length=255)),
                ("city", models.CharField(default="", max_length=100)),
                ("state", models.CharField(default="NA", max_length=2)),
                ("zip_code", models.CharField(default="00000", max_length=10)),
                ("payment_method", models.CharField(default="paypal", max_length=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "profile_picture",
                    models.ImageField(
                        blank=True, null=True, upload_to="profile_pictures/"
                    ),
                ),
                (
                    "linked_account",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subscriber_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
