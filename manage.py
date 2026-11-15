#!/usr/bin/env python
"""Herramienta de línea de comandos para administrar el proyecto Django."""
import os
import sys

if __name__ == '__main__':
    # Selecciona la configuración del proyecto antes de ejecutar el comando.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    # Ejecuta migrate, runserver, seed_demo, createsuperuser y otros comandos.
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
