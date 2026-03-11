#!/bin/bash
# Script para liberar el puerto 8000 en Linux/Mac

echo "========================================"
echo "  Liberando Puerto 8000"
echo "========================================"
echo ""

# Buscar proceso en puerto 8000
PID=$(lsof -ti:8000)

if [ -z "$PID" ]; then
    echo "[INFO] Puerto 8000 ya está libre"
else
    echo "[INFO] Proceso encontrado en puerto 8000: PID $PID"
    echo "[INFO] Terminando proceso..."
    kill -9 $PID
    
    if [ $? -eq 0 ]; then
        echo "[OK] Puerto 8000 liberado exitosamente"
    else
        echo "[ERROR] No se pudo terminar el proceso"
        exit 1
    fi
fi

echo ""
echo "========================================"
