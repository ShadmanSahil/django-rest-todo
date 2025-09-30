from django.db import models

class User(models.Model):
    id = models.BigAutoField(primary_key=True) # change to UUID
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=100, blank=True, default='')
    first_name = models.CharField(max_length=100, blank=True, default='')
    last_name = models.CharField(max_length=100, blank=True, default='')
    birthday = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

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

    firebase_uid = models.CharField(max_length=128, unique=True)

    class Meta:
        ordering = ['id']