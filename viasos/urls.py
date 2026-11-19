"""Mapa de direcciones de la aplicación ViaSOS y su función asociada."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),                         # Página de inicio.
    path('registro/', views.register, name='register'),        # Crear cuenta.
    path('ingresar/', views.login_view, name='login'),         # Iniciar sesión.
    path('salir/', views.logout_view, name='logout'),          # Cerrar sesión.
    path('panel/', views.dashboard, name='dashboard'),         # Panel de usuario.
    path('perfil/guardar/', views.save_profile, name='save_profile'),
    path('contactos/agregar/', views.add_contact, name='add_contact'),
    path('contactos/<int:pk>/eliminar/', views.delete_contact, name='delete_contact'),
    path('qr/crear/', views.create_qr, name='create_qr'),
    path('qr/<str:token>/estado/', views.toggle_qr, name='toggle_qr'),
    path('qr/<str:token>/eliminar/', views.delete_qr, name='delete_qr'),
    path('qr/<str:token>/imagen/', views.qr_image, name='qr_image'),
    path('qr/<str:token>/', views.public_profile, name='public_profile'),
    path('mis-qrs/<str:token>/', views.qr_detail, name='qr_detail'),
    path('soporte/nuevo/', views.create_ticket, name='create_ticket'),
    path('admin-viasos/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-viasos/usuarios/', views.admin_users, name='admin_users'),
    path('admin-viasos/usuarios/<int:pk>/estado/', views.admin_toggle_user, name='admin_toggle_user'),
    path('admin-viasos/configuracion/', views.admin_settings, name='admin_settings'),
    path('admin-viasos/soporte/', views.admin_support, name='admin_support'),
    path('admin-viasos/soporte/<int:pk>/', views.admin_update_ticket, name='admin_update_ticket'),
]
