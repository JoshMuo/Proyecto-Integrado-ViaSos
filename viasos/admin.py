"""Registro de los modelos de ViaSOS en el administrador nativo de Django."""
from django.contrib import admin
from .models import Perfil, Contacto, CodigoQR, Notificacion, Soporte, Configuracion, Pregunta

# Cada modelo queda disponible para consultar, crear, modificar y eliminar registros.
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'relationship', 'user')
    search_fields = ('name', 'phone', 'user__username')

@admin.register(CodigoQR)
class CodigoQRAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'active', 'created_at')
    search_fields = ('name', 'token', 'user__username')
    list_filter = ('active',)

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username', 'text')

@admin.register(Soporte)
class SoporteAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'status', 'created_at')
    search_fields = ('subject', 'user__username')
    list_filter = ('status',)

@admin.register(Configuracion)
class ConfiguracionAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('question', 'published')
    list_filter = ('published',)
    search_fields = ('question',)
