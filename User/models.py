from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    """
    AbstractUser class comes with: 

    username, 
    first_name, 
    last_name, 
    email, 
    is_active, 
    is_staff,
    is_superuser, 
    date_joined, 
    last_login, 
    groups, 
    user_permissions

    """

    id = models.BigAutoField(primary_key=True) # needs to be changed to UUID
    firebase_uid = models.CharField(max_length=128, unique=True)
    phone = models.CharField(max_length=100, blank=True, default='')
    birthday = models.DateField(blank=True, null=True)

    USER_TYPE_CHOICES = (
        ('ADMIN', "Admin"),
        ('USER', 'User'),
    )
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='USER',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']