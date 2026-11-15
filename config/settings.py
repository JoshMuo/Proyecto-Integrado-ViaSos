"""Configuración central de Django para ejecución local de ViaSOS."""
from pathlib import Path
import os

# Rutas físicas del proyecto y clave de firma de sesiones/formularios.
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'viasos-local-development-key-change-before-sharing')
DEBUG = True  # Activado para desarrollo local; desactivar al publicar en producción.
ALLOWED_HOSTS = ['*']  # Permite pruebas desde otros equipos de la misma red local.

# Aplicaciones integradas de Django más la aplicación ViaSOS.
INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    'viasos',
]

# Componentes que procesan peticiones, sesiones, seguridad y mensajes.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]
ROOT_URLCONF = 'config.urls'  # Archivo que distribuye las direcciones web.

# Motor de plantillas: se utiliza un único HTML ubicado en /templates.
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]
WSGI_APPLICATION = 'config.wsgi.application'  # Punto de entrada para servidores WSGI.

# Única base de datos: SQLite, archivo local db.sqlite3 en la carpeta raíz.
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}

# Idioma, zona horaria y formato de claves primarias.
AUTH_PASSWORD_VALIDATORS = []  # Sin validadores adicionales en esta versión de demostración.
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Archivos estáticos, como la hoja CSS sencilla.
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
LOGIN_URL = '/ingresar/'
