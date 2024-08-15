from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    groups = models.ManyToManyField('auth.Group', related_name='nad_users')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='nad_user_permissions')
