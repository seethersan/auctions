from django.urls import path
from users import views

urlpatterns = [
    path('users/', views.UserListCreateAPIView.as_view(), name='api-user-list'),
    path('users/<int:pk>/', views.UserDetailsAPIView.as_view(), name='api-user-details'),
]