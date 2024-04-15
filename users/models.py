from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    photo = models.ImageField(default='default_profile_pic.png')
