from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from apps.tasks.api.serializers import TaskSerializer
from apps.tasks.models import Task


class TaskListCreateAPIView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    )
    filterset_fields = ('is_done',)
    search_fields = ('title',)
    ordering_fields = ('created_at',)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(
                Q(owner=self.request.user) |
                Q(owner__isnull=True)
            )
        return self.queryset.filter(owner__isnull=True)


class TaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(
                Q(owner=self.request.user) |
                Q(owner__isnull=True)
            )
        return self.queryset.filter(owner__isnull=True)
