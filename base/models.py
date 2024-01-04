from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class CustomUserManager (BaseUserManager):

    def create_user(self, email, password = None):
        if not email:
            raise ValueError ("User must have an email")

        user = self.models(email = self.normalize_email(email)) # Formating user email
        user = user.set_password(password) # Hash user password
        user.save(using = self._db) # Responsible for saving created or modified user object into the database
        return user


    
    def create_superuser (self, email, password):
        user = self.create_user(email, password) # Create super user
        user.is_admin = True
        user.save(using = self._db)
        return user



class CustomUser (AbstractBaseUser):

    email = models.EmailField(verbose_name = "email address", max_length = 255, unique = True)
    fullname = models.CharField(max_length = 30)
    phone = models.IntegerField()
    password = models.CharField(max_length = 10)
    is_admin = models.BooleanField(default = False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm (self, perm, obj = None):
        return True

    def has_module_perms (self, app_label):
        return True

    def is_staff (self):
        return self.is_admin