from django.urls import path
from accounts import views
from .views import SignUpView

urlpatterns = [ 
    path("signup/", SignUpView.as_view(), name="signup"),
    path('portfolio/<username>/', views.portfolio, name='portfolio'),
    path('portfolio/<username>/sell', views.sell_etf, name='sell_etf')
]