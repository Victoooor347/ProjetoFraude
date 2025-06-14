# detector/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('alerta/<int:alerta_id>/', views.alerta_detalhe, name='alerta_detalhe'),
    path('alerta/<int:alerta_id>/marcar/<str:novo_status>/', views.marcar_status_alerta, name='marcar_status'),
]