from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from TodoList.listserializers import ListSerializer
from TodoList.models import TodoList
from TodoItem.models import TodoItem

class ListViewSet(viewsets.ModelViewSet):
    queryset = TodoList.objects.prefetch_related("items").all()
    serializer_class = ListSerializer