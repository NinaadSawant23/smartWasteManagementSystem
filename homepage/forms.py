from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from .models import Subscriber, PickupRequest, Driver, RedemptionWorker


class UserRegistrationForm(UserCreationForm):
    fname = forms.CharField(max_length=100, label="First Name")
    lname = forms.CharField(max_length=100, label="Last Name")
    phone = forms.CharField(max_length=15, label="Phone Number")
    email = forms.EmailField(label="Email Address")
    street_address = forms.CharField(max_length=255, label="Street Address")
    city = forms.CharField(max_length=100, label="City")
    state = forms.ChoiceField(choices=[
        ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'),
        ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'),
        ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'),
        ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'),
        ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
        ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'),
        ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'),
        ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),
        ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
        ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'),
        ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'),
        ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'), ('WY', 'Wyoming')
    ], label="State")
    zip_code = forms.CharField(max_length=10, label="Zip Code")
    payment_method = forms.ChoiceField(choices=[
        ('cashapp', 'CashApp'),
        ('venmo', 'Venmo'),
        ('zelle', 'Zelle')
    ], label="Payment Method")

    class Meta:
        model = User
        fields = ['username', 'fname', 'lname', 'email', 'phone', 'street_address', 'city', 'state', 'zip_code',
                  'payment_method', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['fname']
        user.last_name = self.cleaned_data['lname']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            Subscriber.objects.create(
                linked_account=user,
                account_id=user.id,
                fname=self.cleaned_data['fname'],
                lname=self.cleaned_data['lname'],
                email=self.cleaned_data['email'],
                phone=self.cleaned_data['phone'],
                street_address=self.cleaned_data['street_address'],
                city=self.cleaned_data['city'],
                state=self.cleaned_data['state'],
                zip_code=self.cleaned_data['zip_code'],
                payment_method=self.cleaned_data['payment_method']
            )
        return user


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message'}),
                              required=True)


class PickupRequestForm(forms.ModelForm):
    class Meta:
        model = PickupRequest
        fields = ['ready_for_pickup', 'num_bags']
        widgets = {
            'ready_for_pickup': forms.Select(choices=[(True, 'Yes'), (False, 'No')]),
            'num_bags': forms.NumberInput(attrs={'min': 0}),
        }


class DriverRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=100, label="Name")
    phone = forms.CharField(max_length=15, label="Phone Number")
    email = forms.EmailField(label="Email Address")

    class Meta:
        model = User
        fields = ['username', 'name', 'phone', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Driver.objects.create(
                linked_account=user,
                name=self.cleaned_data['name'],
                phone=self.cleaned_data['phone'],
                email=self.cleaned_data['email']
            )
        return user

class RedemptionWorkerRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=100, label="Name")
    phone = forms.CharField(max_length=15, label="Phone Number")
    email = forms.EmailField(label="Email Address")

    class Meta:
        model = User
        fields = ['username', 'name', 'phone', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            RedemptionWorker.objects.create(
                linked_account=user,
                name=self.cleaned_data['name'],
                phone=self.cleaned_data['phone'],
                email=self.cleaned_data['email']
            )
        return user

class SubscriberUpdateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}),
        required=False,
        label="New Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}),
        required=False,
        label="Confirm Password"
    )

    class Meta:
        model = Subscriber
        fields = [
            'fname', 'lname', 'email', 'phone', 'street_address', 'city', 'state',
            'zip_code', 'payment_method'
        ]
        widgets = {
            'state': forms.Select(choices=[(state, state) for state in [
                'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY',
                'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND',
                'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
            ]]),
            'payment_method': forms.Select(choices=[
                ('cashapp', 'CashApp'),
                ('venmo', 'Venmo'),
                ('zelle', 'Zelle'),
            ]),
        }

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get('zip_code')
        if not zip_code.isdigit() or len(zip_code) != 5:
            raise forms.ValidationError("Enter a valid 5-digit ZIP code.")
        return zip_code

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Subscriber.objects.filter(email=email).exclude(account_id=self.instance.account_id).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password:
            try:
                validate_password(password, user=self.instance.linked_account)
            except ValidationError as e:
                self.add_error('password', e)

            if password != confirm_password:
                self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data