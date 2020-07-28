from django.urls import path
from stocks import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('companies/', views.companies, name='companies'),
]
