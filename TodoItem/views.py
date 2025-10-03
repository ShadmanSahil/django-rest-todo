from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from TodoItem.itemserializers import ItemSerializer
from TodoItem.models import TodoItem
from rest_framework.permissions import IsAuthenticated


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    permission_class = [IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        if user.is_staff==True:
            return TodoItem.objects.all()
        else:
            return TodoItem.objects.filter(assignee=user)