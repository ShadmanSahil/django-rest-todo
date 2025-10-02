from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from TodoList.listserializers import ListSerializer
from TodoList.models import TodoList
from TodoItem.models import TodoItem
from rest_framework.permissions import IsAuthenticated


class ListViewSet(viewsets.ModelViewSet):
    serializer_class = ListSerializer
    permission_class = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff==True:
            return TodoList.objects.prefetch_related("items").all()
        else:
            return TodoList.objects.prefetch_related("items").filter(owner=user)