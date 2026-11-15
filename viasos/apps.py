"""Configuración de la aplicación ViaSOS para el registro de Django."""
from django.apps import AppConfig

class ViasosConfig(AppConfig):
    # Tipo de clave primaria por defecto y nombre interno de la aplicación.
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'viasos'
