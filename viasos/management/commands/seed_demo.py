"""Carga seis cuentas ficticias y registros básicos para presentar ViaSOS."""
import secrets
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from viasos.models import Perfil, Contacto, CodigoQR, Notificacion, Configuracion, Soporte, Pregunta

class Command(BaseCommand):
    help = 'Crea las seis cuentas de demostración sin duplicarlas.'

    def handle(self, *args, **kwargs):
        # Correo, contraseña y rol de cada cuenta de demostración.
        cuentas = [
            ('Administrador', 'ViaSOS', 'admin@viasos.local', 'ViaSOS_Admin_2026!', 'admin'),
            ('Camila', 'Rojas', 'camila.rojas@demo.viasos.local', 'ViaSOS_Demo_2026!', 'user'),
            ('Matías', 'Fuentes', 'matias.fuentes@demo.viasos.local', 'ViaSOS_Demo_2026!', 'user'),
            ('Valentina', 'Soto', 'valentina.soto@demo.viasos.local', 'ViaSOS_Demo_2026!', 'user'),
            ('Diego', 'Muñoz', 'diego.munoz@demo.viasos.local', 'ViaSOS_Demo_2026!', 'user'),
            ('Antonia', 'Vargas', 'antonia.vargas@demo.viasos.local', 'ViaSOS_Demo_2026!', 'user'),
        ]

        for index, (nombre, apellido, correo, clave, rol) in enumerate(cuentas):
            # get_or_create evita duplicar cuentas al ejecutar el comando varias veces.
            usuario, creado = User.objects.get_or_create(
                username=correo,
                defaults={'email': correo, 'first_name': nombre, 'last_name': apellido},
            )
            # La contraseña se asigna solo al crear la cuenta: no se modifica una ya existente.
            if creado:
                usuario.set_password(clave)

            # Django exige ambos permisos para permitir el acceso al admin nativo.
            if rol == 'admin':
                usuario.is_staff = True
                usuario.is_superuser = True
            usuario.save()

            # Cada cuenta tiene un perfil ViaSOS relacionado uno a uno con User.
            perfil, _ = Perfil.objects.get_or_create(user=usuario, defaults={'role': rol})
            if rol == 'admin':
                perfil.role = 'admin'
                perfil.save()
            elif creado:
                # Datos ficticios opcionales para mostrar ejemplos durante la presentación.
                if index == 1:
                    perfil.allergies = 'Penicilina'
                    perfil.public_allergies = True
                if index == 3:
                    perfil.conditions = 'Asma'
                    perfil.medications = 'Inhalador'
                    perfil.public_conditions = True
                    perfil.public_medications = True
                if index == 4:
                    perfil.blood_type = 'A+'
                    perfil.public_blood_type = True
                perfil.save()
                Contacto.objects.create(user=usuario, name='Contacto de emergencia', phone='+56912345678', relationship='Otro familiar')
                CodigoQR.objects.create(user=usuario, token=secrets.token_urlsafe(18), name='Mi QR 1', description='QR de demostración', active=(index != 5))
                Notificacion.objects.create(user=usuario, text='Bienvenido a la demostración de ViaSOS.')

            self.stdout.write(('Creada: ' if creado else 'Ya existe: ') + correo)

        # Configuración de demostración de WhatsApp.
        Configuracion.objects.get_or_create(key='whatsapp_mode', defaults={'value': 'simulation'})

        # Tickets ficticios para probar la sección de soporte del administrador.
        correos_demo = [
            'camila.rojas@demo.viasos.local',
            'matias.fuentes@demo.viasos.local',
            'valentina.soto@demo.viasos.local',
        ]
        ejemplos_tickets = [
            ('Consulta sobre mi código QR', 'pending'),
            ('Actualización de información', 'in_review'),
            ('Prueba de soporte resuelta', 'resolved'),
        ]
        for index, (asunto, estado) in enumerate(ejemplos_tickets):
            propietario = User.objects.get(username=correos_demo[index])
            Soporte.objects.get_or_create(
                user=propietario,
                subject=asunto,
                defaults={'body': 'Solicitud ficticia para demostración.', 'status': estado},
            )

        # Preguntas frecuentes de ejemplo, solo si la tabla todavía está vacía.
        if not Pregunta.objects.exists():
            ejemplos = [
                ('¿Qué es ViaSOS?', 'Una ficha de emergencia accesible mediante un código QR.'),
                ('¿Necesito instalar una aplicación?', 'No. La ficha se abre en el navegador.'),
                ('¿Qué información se muestra?', 'Solo los datos autorizados por el titular.'),
            ]
            for pregunta, respuesta in ejemplos:
                Pregunta.objects.create(question=pregunta, answer=respuesta)

        self.stdout.write(self.style.SUCCESS(
            'Administrador: admin@viasos.local / ViaSOS_Admin_2026! | '
            'Usuarios: contraseña ViaSOS_Demo_2026!'
        ))
