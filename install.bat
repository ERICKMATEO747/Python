@echo off
REM Script de instalación rápida para Windows
REM Flevo Backend Setup

echo ========================================
echo   Flevo Backend - Setup Automatizado
echo ========================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado
    echo Por favor instala Python 3.8 o superior desde https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

REM Ejecutar script de setup
echo Ejecutando setup automatizado...
python setup.py

if errorlevel 1 (
    echo.
    echo [ERROR] Setup fallido
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Setup completado exitosamente
echo ========================================
echo.
echo Para activar el entorno virtual:
echo   venv\Scripts\activate
echo.
echo Para ejecutar el servidor:
echo   python main.py
echo.
pause
