#!/bin/bash
# Script de instalación rápida para Linux/Mac
# Flevo Backend Setup

echo "========================================"
echo "  Flevo Backend - Setup Automatizado"
echo "========================================"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 no está instalado"
    echo "Por favor instala Python 3.8 o superior"
    exit 1
fi

echo "[OK] Python encontrado: $(python3 --version)"
echo ""

# Ejecutar script de setup
echo "Ejecutando setup automatizado..."
python3 setup.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Setup fallido"
    exit 1
fi

echo ""
echo "========================================"
echo "  Setup completado exitosamente"
echo "========================================"
echo ""
echo "Para activar el entorno virtual:"
echo "  source venv/bin/activate"
echo ""
echo "Para ejecutar el servidor:"
echo "  python main.py"
echo ""
