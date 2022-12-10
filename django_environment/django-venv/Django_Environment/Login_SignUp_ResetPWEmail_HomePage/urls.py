"""Django_LogIn_UserAuth_Alison URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from .views import auth_view, verify_view
from django.contrib.auth.views import LogoutView
from etfs import views as etf_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("etf/", include("etfs.urls")),
    path('', TemplateView.as_view(template_name='home.html'), name='home_view'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('login/', auth_view, name='login'),
    path('verify/', verify_view, name='verify_view'),
    path('etf/browse/', etf_views.etf_browse, name='browse_view'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('paypal/', include('paypal.standard.ipn.urls')),
]
