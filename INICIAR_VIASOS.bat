@echo off
setlocal
REM ============================================================
REM INICIO DE VIASOS
REM Usa exclusivamente el Python instalado dentro de .venv.
REM Abre el navegador y mantiene el servidor activo en esta ventana.
REM ============================================================
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: No existe el entorno virtual .venv.
    echo Ejecuta primero INSTALAR_VIASOS.bat y espera a que termine.
    pause
    exit /b 1
)
set "PYTHON_VENV=%CD%\.venv\Scripts\python.exe"

echo.
echo Comprobando la base de datos...
"%PYTHON_VENV%" manage.py migrate
if errorlevel 1 (
    echo ERROR: No se pudieron aplicar las migraciones.
    pause
    exit /b 1
)

REM Verifica las cuentas demo y los permisos de superusuario Django.
"%PYTHON_VENV%" manage.py seed_demo
if errorlevel 1 (
    echo ERROR: No se pudieron verificar las cuentas de demostracion.
    pause
    exit /b 1
)

REM Abre la pagina principal en el navegador predeterminado.
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:8000/"

echo.
echo ViaSOS esta disponible en http://127.0.0.1:8000/
echo Administrador Django: http://127.0.0.1:8000/admin/
echo Para detener el servidor, presiona CTRL+C.
echo.

REM Ejecuta Django usando el interprete del entorno virtual.
"%PYTHON_VENV%" manage.py runserver 0.0.0.0:8000
pause
endlocal
