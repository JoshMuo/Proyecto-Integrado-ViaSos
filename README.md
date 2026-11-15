# ViaSOS — versión simple y comentada

Versión local simplificada. Usa **SQLite**, incluida con Python/Django; no requiere MongoDB, Atlas ni PyMongo.

## Instalación en Windows
1. Descomprima el ZIP.
2. Abra la carpeta `VIASOS_SIMPLE` en Visual Studio Code.
3. Ejecute `INSTALAR_VIASOS.bat` una sola vez.
4. Ejecute `INICIAR_VIASOS.bat` cada vez que quiera usar el sistema.
5. Se abrirá `http://127.0.0.1:8000/` en el navegador.

## Administradores
- Panel administrativo de ViaSOS: `http://127.0.0.1:8000/admin-viasos/`
- Administrador nativo de Django: `http://127.0.0.1:8000/admin/`
- Usuario: `admin@viasos.local`
- Contraseña: `ViaSOS_Admin_2026!`

El comando `python manage.py seed_demo` conserva las contraseñas existentes y asegura que la cuenta administradora tenga `is_staff=True` e `is_superuser=True`, necesarios para entrar al admin nativo.

## Usuarios de demostración
Los cinco usuarios mantienen la contraseña común `ViaSOS_Demo_2026!`:
- camila.rojas@demo.viasos.local
- matias.fuentes@demo.viasos.local
- valentina.soto@demo.viasos.local
- diego.munoz@demo.viasos.local
- antonia.vargas@demo.viasos.local

## Estructura y propósito de archivos
- `manage.py`: ejecuta comandos administrativos de Django.
- `config/settings.py`: aplicaciones, middleware, idioma, rutas de plantillas y SQLite.
- `config/urls.py`: conecta `/admin/` con el administrador nativo y el resto con ViaSOS.
- `config/wsgi.py`: punto de entrada WSGI para servidores compatibles.
- `viasos/models.py`: estructura de los datos y relaciones almacenadas en SQLite.
- `viasos/views.py`: lógica que atiende formularios, sesiones, perfiles, contactos, QR y soporte.
- `viasos/urls.py`: relación entre cada dirección web y su función.
- `viasos/admin.py`: registra los modelos de ViaSOS en el administrador Django.
- `viasos/management/commands/seed_demo.py`: crea los perfiles y datos de demostración sin duplicarlos.
- `viasos/migrations/`: historial de cambios de estructura de la base de datos.
- `templates/viasos.html`: **único archivo HTML**. Las secciones se muestran según la variable `section` que entrega cada vista. Los comentarios HTML identifican cada pantalla y su función.
- `static/css/viasos.css`: hoja de estilos pequeña y comentada por bloques.
- `requirements.txt`: dependencias Python necesarias.
- `INSTALAR_VIASOS.bat`: prepara el entorno, instala paquetes, migra y carga datos de prueba.
- `INICIAR_VIASOS.bat`: activa el entorno, aplica migraciones e inicia servidor y navegador.
- `db.sqlite3`: base de datos local creada automáticamente; no se incluye como requisito del proyecto.

## Importante
Esta es una versión para desarrollo y demostración local. `DEBUG=True` y `ALLOWED_HOSTS=['*']` no deben mantenerse así en un despliegue público. La ficha QR necesita que el dispositivo que escanea pueda acceder a la dirección IP del equipo que ejecuta Django; `127.0.0.1` solo funciona en el mismo equipo.

## Solución de problemas del instalador (Windows)
Los archivos BAT usan `python` y el ejecutable `.venv\\Scripts\\python.exe`; no dependen del comando `py`.
Si aparece que no existe `.venv`, ejecuta `INSTALAR_VIASOS.bat` y verifica que termine con el mensaje "Instalacion terminada correctamente". No ejecutes `INICIAR_VIASOS.bat` hasta entonces.
