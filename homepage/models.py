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
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def _str_(self):
        return self.fname
