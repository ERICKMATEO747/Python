#!/bin/bash
# Script de inicio rápido con verificación automática
# Flevo Backend

echo "========================================"
echo "  Flevo Backend - Inicio Rápido"
echo "========================================"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "main.py" ]; then
    echo "[ERROR] No se encuentra main.py"
    echo "Por favor ejecuta este script desde el directorio raíz del proyecto"
    exit 1
fi

# Verificar entorno virtual
if [ ! -d "venv" ]; then
    echo "[ERROR] Entorno virtual no encontrado"
    echo ""
    echo "Ejecuta primero: ./install.sh"
    exit 1
fi

# Activar entorno virtual
echo "[INFO] Activando entorno virtual..."
source venv/bin/activate

# Verificar si existe .env
if [ ! -f ".env" ]; then
    echo ""
    echo "========================================"
    echo "  ADVERTENCIA: Archivo .env no encontrado"
    echo "========================================"
    echo ""
    echo "El servidor se ejecutará con valores por defecto"
    echo "Solo para DESARROLLO - NO usar en producción"
    echo ""
    echo "Para configurar correctamente:"
    echo "  1. cp .env.example .env"
    echo "  2. Edita .env con tus configuraciones"
    echo ""
    sleep 3
fi

# Liberar puerto 8000 si está ocupado
echo "[INFO] Verificando puerto 8000..."
PID=$(lsof -ti:8000 2>/dev/null)
if [ ! -z "$PID" ]; then
    echo "[INFO] Puerto 8000 ocupado, liberando..."
    kill -9 $PID 2>/dev/null
fi

# Ejecutar servidor
echo ""
echo "========================================"
echo "  Iniciando servidor..."
echo "========================================"
echo ""
echo "Servidor: http://localhost:8000"
echo "Documentación: http://localhost:8000/docs"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

python main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "========================================"
    echo "  ERROR al iniciar el servidor"
    echo "========================================"
    echo ""
    echo "Verifica:"
    echo "  1. Dependencias instaladas: pip install -r requirements.txt"
    echo "  2. Configuración correcta en .env"
    echo "  3. Base de datos accesible"
    echo ""
    echo "Ejecuta para diagnóstico: python verify_config.py"
    echo ""
    exit 1
fi
