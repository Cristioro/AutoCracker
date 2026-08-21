#!/bin/bash

echo "========================================================"
echo "Eliminando AutoCracker de Nautilus Scripts..."
echo "========================================================"

NAUTILUS_SUBDIR="$HOME/.local/share/nautilus/scripts/AutoCracker"

# Borrar la carpeta entera
if [ -d "$NAUTILUS_SUBDIR" ]; then
    rm -rf "$NAUTILUS_SUBDIR"
    echo "✅ Carpeta 'AutoCracker' eliminada correctamente."
else
    echo "ℹ️ La carpeta no existía, nada que eliminar."
fi

echo "========================================================"