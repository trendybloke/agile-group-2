from django.urls import path, include
from sadmin import views

urlpatterns = [
    path('users/', views.Users.as_view(), name='users'),
    path('user/<int:pk>', views.UserDetailView,name="customuser_detail"),
]