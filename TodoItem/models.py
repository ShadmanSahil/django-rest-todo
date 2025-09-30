from django.db import models
from User.models import User

class TodoItem(models.Model):
    STATUS_CHOICES = (
        ('PENDING', "Pending"),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    )

    id = models.BigAutoField(primary_key=True) # UUID + manytomany
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, default='')
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='DONE',
    )
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_items")
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']