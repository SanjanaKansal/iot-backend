from django.contrib.auth.models import User
from django.db import models


class UserTypes(models.IntegerChoices):
    ADMIN = 1
    FACILITY_MANAGER = 2
    FACILITY_STAFF = 3
    END_USER = 4


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization_id = models.CharField(max_length=1024)
    user_type = models.IntegerField(choices=UserTypes.choices, default=UserTypes.ADMIN)
    token = models.CharField(max_length=1024)
    is_verified = models.BooleanField(default=False)
