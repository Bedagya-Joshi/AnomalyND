from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    groups = models.ManyToManyField('auth.Group', related_name='nad_users')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='nad_user_permissions')

class CapturedPacket(models.Model):
    src_ip = models.CharField(max_length=15)
    dst_ip = models.CharField(max_length=15)
    port = models.IntegerField(null=True, blank=True)
    protocol = models.CharField(max_length=10)
    length = models.IntegerField()
    info = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)