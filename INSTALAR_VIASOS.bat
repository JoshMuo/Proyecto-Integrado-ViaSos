@echo off
setlocal
REM ============================================================
REM INSTALADOR DE VIASOS
REM Crea el entorno virtual local e instala las dependencias.
REM Usa el comando 'python' para evitar depender del launcher 'py'.
REM ============================================================
cd /d "%~dp0"

echo.
echo [1/4] Comprobando Python...
python --version
if errorlevel 1 (
    echo ERROR: No se encontro Python en PATH.
    echo Instala Python 3.11 o superior y activa "Add Python to PATH".
    pause
    exit /b 1
)

echo.
echo [2/4] Creando entorno virtual .venv...
if not exist ".venv\Scripts\python.exe" (
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno virtual.
        echo Comprueba que Python tenga instalado el modulo venv.
        pause
        exit /b 1
    )
) else (
    echo El entorno virtual ya existe; se reutilizara.
)

set "PYTHON_VENV=%CD%\.venv\Scripts\python.exe"
if not exist "%PYTHON_VENV%" (
    echo ERROR: No se encontro el Python del entorno virtual.
    pause
    exit /b 1
)

echo.
echo [3/4] Instalando dependencias...
"%PYTHON_VENV%" -m pip install --upgrade pip
if errorlevel 1 (
    echo ERROR: No se pudo actualizar pip.
    pause
    exit /b 1
)
"%PYTHON_VENV%" -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias.
    pause
    exit /b 1
)

echo.
echo [4/4] Preparando base de datos y cuentas de demostracion...
"%PYTHON_VENV%" manage.py migrate
if errorlevel 1 (
    echo ERROR: Fallaron las migraciones de Django.
    pause
    exit /b 1
)
"%PYTHON_VENV%" manage.py seed_demo
if errorlevel 1 (
    echo ERROR: No se pudieron crear/verificar las cuentas de demostracion.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Instalacion terminada correctamente.
echo Ahora ejecuta INICIAR_VIASOS.bat para abrir ViaSOS.
echo ============================================================
pause
endlocal
