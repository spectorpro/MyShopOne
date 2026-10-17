from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True)
    phone = models.CharField('phone number', max_length=20, blank=True)
    country = models.CharField('country', max_length=100, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
