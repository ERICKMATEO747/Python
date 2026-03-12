@echo off
REM Script de inicio rápido con verificación automática
REM Flevo Backend

echo ========================================
echo   Flevo Backend - Inicio Rapido
echo ========================================
echo.

REM Verificar que estamos en el directorio correcto
if not exist "main.py" (
    echo [ERROR] No se encuentra main.py
    echo Por favor ejecuta este script desde el directorio raiz del proyecto
    pause
    exit /b 1
)

REM Verificar entorno virtual
if not exist "venv\" (
    echo [ERROR] Entorno virtual no encontrado
    echo.
    echo Ejecuta primero: install.bat
    pause
    exit /b 1
)

REM Activar entorno virtual
echo [INFO] Activando entorno virtual...
call venv\Scripts\activate

REM Verificar si existe .env
if not exist ".env" (
    echo.
    echo ========================================
    echo   ADVERTENCIA: Archivo .env no encontrado
    echo ========================================
    echo.
    echo El servidor se ejecutara con valores por defecto
    echo Solo para DESARROLLO - NO usar en produccion
    echo.
    echo Para configurar correctamente:
    echo   1. copy .env.example .env
    echo   2. Edita .env con tus configuraciones
    echo.
    timeout /t 5
)

REM Liberar puerto 8000 si está ocupado
echo [INFO] Verificando puerto 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo [INFO] Puerto 8000 ocupado, liberando...
    taskkill /PID %%a /F >nul 2>&1
)

REM Ejecutar servidor
echo.
echo ========================================
echo   Iniciando servidor...
echo ========================================
echo.
echo Servidor: http://localhost:8000
echo Documentacion: http://localhost:8000/docs
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python main.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo   ERROR al iniciar el servidor
    echo ========================================
    echo.
    echo Verifica:
    echo   1. Dependencias instaladas: pip install -r requirements.txt
    echo   2. Configuracion correcta en .env
    echo   3. Base de datos accesible
    echo.
    echo Ejecuta para diagnostico: python verify_config.py
    echo.
    pause
    exit /b 1
)
