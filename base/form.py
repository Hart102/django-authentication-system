from django.forms import ModelForm
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

# User Creation Form
class MyUserCreationForm(UserCreationForm):
    firstname = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'tim'}))
    lastname = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'brown'}))
    email = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'tim@gmail.com'}))
    phoneNumber = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': '+234 901 234 56'}))
    password1 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'TimBrown123@'}))
    password2 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'TimBrown123@'}))

    class Meta:
        model = User
        fields = ["firstname", "lastname", "email", "phoneNumber", "password1", "password2"]

    def clean_username(self):
        return self.clean_email()

    def clean_email(self):
        return self.cleaned_data.get("email").lower()

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ["firstname", "lastname", "email", "phoneNumber"]

class UpdateImage(ModelForm):
    class Meta:
        model = User
        fields = ["avatar", "firstname", "lastname", "email", "phoneNumber"]