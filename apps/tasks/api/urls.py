from django.urls import path

from apps.tasks.api.views import TaskListCreateAPIView, TaskRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', TaskListCreateAPIView.as_view()),
    path('<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view()),
]
