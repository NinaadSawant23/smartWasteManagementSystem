from django.db import models

class Subscriber(models.Model):
    linked_account = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='subscriber_profile', null = True)
    account_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    street_address = models.CharField(max_length=255, default="")  
    city = models.CharField(max_length=100, default="")  
    state = models.CharField(max_length=2, default="NA")  
    zip_code = models.CharField(max_length=10, default="00000")  
    payment_method = models.CharField(max_length=10, default="paypal")  
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.fname


class ContactSubmission(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"