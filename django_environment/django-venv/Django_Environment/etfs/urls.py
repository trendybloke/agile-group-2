from django.urls import path, include
from etfs import views

urlpatterns = [
    path('browse', views.etf_browse, name='browse_etfs'),
    path('details/<etf_symbol>/', views.etf_details, name='etf_details'),
    path('purchase/<etf_symbol>/', views.purchase_etf, name='purchase_etf'),
    path('purchase/new/<etf_symbol>/', views.instantiate_etf, name='instantiate_etf')
]
