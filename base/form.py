from django.forms import ModelForm
from .models import CustomUser

class PhotoForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'