from django.urls import path
from accounts import views
from .views import SignUpView
from .views import register_user

urlpatterns = [ 
    path("signup/", SignUpView.as_view(), name="signup"),
    path('portfolio/<username>/', views.portfolio, name='portfolio'),
    path('portfolio/<username>/sell', views.sell_etf, name='sell_etf'),
    path('register/', register_user, name="register"),
]