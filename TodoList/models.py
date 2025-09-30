from django.db import models
from User.models import User
from TodoItem.models import TodoItem

class TodoList(models.Model):
    # id = models.UUIDField(primary_key=True)
    id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todo_lists")
    items = models.ManyToManyField(TodoItem, related_name="items", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']