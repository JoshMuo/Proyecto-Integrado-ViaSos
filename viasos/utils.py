"""Funciones auxiliares pequeñas disponibles para la aplicación ViaSOS."""
import secrets
from django.utils import timezone

# Devuelve la fecha y hora actual respetando la zona horaria de Django.
def now():
    return timezone.now()

# Crea una cadena aleatoria segura que puede utilizarse como token QR.
def new_token():
    return secrets.token_urlsafe(24)
