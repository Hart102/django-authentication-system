from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    firstname = models.CharField(max_length = 200, default="")
    lastname = models.CharField(max_length = 200, default="")
    phoneNumber = models.IntegerField(default = 0)
    email = models.EmailField(unique=True, null=True)
    avatar = models.ImageField(null = True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
