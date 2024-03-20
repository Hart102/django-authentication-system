from django.forms import ModelForm
from .models import User
from django.contrib.auth.forms import UserCreationForm

# User Creation Form
class MyUserCreationForm(UserCreationForm):
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