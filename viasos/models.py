"""Modelos de datos de ViaSOS. Django guarda estos registros en SQLite local."""
from django.db import models
from django.contrib.auth.models import User

# Perfil extendido: los datos opcionales solo se publican si su casilla está activa.
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='viasos')
    role = models.CharField(max_length=10, default='user')
    phone = models.CharField(max_length=40, blank=True)
    address = models.CharField(max_length=255, blank=True)
    birth_date = models.CharField(max_length=20, blank=True)
    allergies = models.TextField(blank=True)
    conditions = models.TextField(blank=True)
    medications = models.TextField(blank=True)
    blood_type = models.CharField(max_length=20, blank=True)
    other = models.TextField(blank=True)
    public_phone = models.BooleanField(default=False)
    public_address = models.BooleanField(default=False)
    public_birth_date = models.BooleanField(default=False)
    public_allergies = models.BooleanField(default=False)
    public_conditions = models.BooleanField(default=False)
    public_medications = models.BooleanField(default=False)
    public_blood_type = models.BooleanField(default=False)
    public_other = models.BooleanField(default=False)

# Contactos privados que se administran desde el panel del propietario.
class Contacto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=40)
    relationship = models.CharField(max_length=40)
    position = models.PositiveSmallIntegerField(default=1)

# QR individual: token público, propietario, estado y datos descriptivos.
class CodigoQR(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Avisos internos asociados a una cuenta.
class Notificacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# Solicitudes de ayuda enviadas por usuarios y respondidas por administración.
class Soporte(models.Model):
    ESTADOS = [('pending', 'Pendiente'), ('in_review', 'En revisión'), ('resolved', 'Resuelto')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=180)
    body = models.TextField()
    status = models.CharField(max_length=20, choices=ESTADOS, default='pending')
    reply = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Configuración simple clave/valor, por ejemplo el modo de WhatsApp.
class Configuracion(models.Model):
    key = models.CharField(max_length=80, unique=True)
    value = models.CharField(max_length=100, default='simulation')

# Preguntas frecuentes que pueden mantenerse desde el admin de Django.
class Pregunta(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    published = models.BooleanField(default=True)
