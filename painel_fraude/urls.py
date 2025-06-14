# painel_fraude/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contas/', include('django.contrib.auth.urls')),
    path('', include('detector.urls')), # Inclui as URLs do nosso app
]