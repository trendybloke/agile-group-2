from django.urls import path
from accounts import views
from .views import login_view, register_user
from django.contrib.auth.views import LogoutView

urlpatterns = [ 
    path('portfolio/<username>/', views.portfolio, name='portfolio'),
    path('portfolio/<username>/sell', views.sell_etf, name='sell_etf'),
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout")
]