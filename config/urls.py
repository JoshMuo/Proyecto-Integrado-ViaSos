"""Rutas principales del proyecto ViaSOS."""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Administrador nativo de Django (gestión directa de modelos y registros).
    path('admin/', admin.site.urls),
    # Rutas funcionales de la aplicación ViaSOS.
    path('', include('viasos.urls')),
]
