from django.forms import ModelForm
from .models import CustomUser

class RegistrationForm (ModelForm):
    class Meta:
        model = CustomUser
        fields = "__all__"
        exclude = ["is_admin", "last_login"]