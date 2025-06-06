from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Customer
from django.contrib.auth import password_validation
from django.utils.translation import gettext, gettext_lazy as _

class CustomerRegistrationForm (UserCreationForm):
    email = forms.CharField( required=True, widget=forms.EmailInput(attrs= {'class':'form-control'} ))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput (attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput (attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        labels = {'email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'})}

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=('Old Password'), strip=False,widget=forms.PasswordInput(attrs={'auto_complete':'current-password','auto_focus':True, 'class':'form-control'}))
    new_password1 = forms.CharField(label=('New Password'), strip=False,widget=forms.PasswordInput(attrs={'auto_complete':'new-password', 'class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=('Confirm Password'), strip=False,widget=forms.PasswordInput(attrs={'auto_complete':'new-password', 'class':'form-control'}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=('Email'), max_length=254,widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=('New Password'), strip=False,widget=forms.PasswordInput(attrs={'auto_complete':'new-password', 'class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=('Confirm Password'), strip=False,widget=forms.PasswordInput(attrs={'auto_complete':'new-password', 'class':'form-control'}))


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','locality','city','zipcode','state' ]
        labels = {'locality':'Address'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
        }







