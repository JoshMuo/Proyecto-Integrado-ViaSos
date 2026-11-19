"""Punto de entrada WSGI para servidores compatibles con Django."""
import os
from django.core.wsgi import get_wsgi_application

# Indica a Django qué módulo contiene los ajustes del proyecto.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# Aplicación WSGI que el servidor web carga para atender peticiones.
application = get_wsgi_application()
