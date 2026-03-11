@echo off
REM Script para liberar el puerto 8000 en Windows

echo ========================================
echo   Liberando Puerto 8000
echo ========================================
echo.

REM Buscar proceso en puerto 8000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    set PID=%%a
)

if defined PID (
    echo [INFO] Proceso encontrado en puerto 8000: PID %PID%
    echo [INFO] Terminando proceso...
    taskkill /PID %PID% /F
    
    if errorlevel 1 (
        echo [ERROR] No se pudo terminar el proceso
        pause
        exit /b 1
    )
    
    echo [OK] Puerto 8000 liberado exitosamente
) else (
    echo [INFO] Puerto 8000 ya esta libre
)

echo.
echo ========================================
pause
