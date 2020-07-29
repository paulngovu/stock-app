from django.urls import path
from stocks import views

urlpatterns = [
    path('', views.viewDashboard, name='dashboard'),
    path('companies/', views.viewCompanies, name='companies'),
    path('search/', views.viewSearch, name='search'),
]
