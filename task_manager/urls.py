from django.urls import path, include
from rest_framework.authtoken import views


urlpatterns = [
    path('api/login/', views.obtain_auth_token),
    path('api/tasks/', include('apps.tasks.api.urls')),
]
