from django import forms
from .models import Account
from django.core.validators import EmailValidator, RegexValidator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(validators=[EmailValidator()])  # Custom defined email field

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        # Example: adding a regex validator to the username
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


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['bio', 'birthday', 'desired_products']

    # def __init__(self, *args, **kwargs):
    #     super(AccountForm, self).__init__(*args, **kwargs)
    #     #self.fields['birthday'].validators.append()


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
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

