from django import forms
from .models import Profile
from django.core.validators import EmailValidator, RegexValidator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(validators=[EmailValidator()])

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].validators.append(
            RegexValidator(
                regex=r'^[A-Za-z\d@_.+-]{1,150}$',
                message='Please, stick to requirements below',
                code='invalid_username'
            )
        )

        self.fields['password1'].validators.append(
            RegexValidator(
                regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&(*)]{8,}$',
                message='Please, stick to requirements below',
                code='invalid_username'
            )
        )

        self.fields['password2'].validators.append(
            RegexValidator(
                regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&(*)]{8,}$',
                message='Please, stick to requirements above',
                code='invalid_username'
            )
        )


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'birthday', 'cart']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(
            RegexValidator(
                regex=r'^[A-Za-z\d@_.+-]{1,150}$',
                message='Please, stick to requirements below',
                code='invalid_username'
            )
        )

class PaymentInfoForm(forms.Form):
    name_on_card = forms.CharField(max_length=100)
    card_number = forms.CharField(max_length=16, validators=[
        RegexValidator(
            regex=r'^\d{16}$',
            message='Card number must be 16 digits',
            code='invalid_card_number'
        )
    ])
    expiration_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    cvv = forms.CharField(max_length=4, validators=[
        RegexValidator(
            regex=r'^\d{3,4}$',
            message='CVV must be 3 or 4 digits',
            code='invalid_cvv'
        )
    ])
    billing_address = forms.CharField(widget=forms.Textarea)