#!/bin/bash

# Obtener la ruta donde está este script (la raíz del AutoCracker)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "========================================================"
echo "Instalando AutoCracker en Nautilus (Carpeta Scripts)..."
echo "========================================================"

# 1. Crear la carpeta base de scripts de Nautilus y la subcarpeta del proyecto
NAUTILUS_SCRIPT_DIR="$HOME/.local/share/nautilus/scripts"
NAUTILUS_SUBDIR="$NAUTILUS_SCRIPT_DIR/AutoCracker"

mkdir -p "$NAUTILUS_SUBDIR"

# 2. Definir el contenido de los scripts
create_script() {
    local NOMBRE="$1"
    local COMANDO="$2"
    local RUTA_DESTINO="$NAUTILUS_SUBDIR/$NOMBRE"

    cat > "$RUTA_DESTINO" <<EOF
#!/bin/bash

# Obtener la ruta de la carpeta seleccionada (decodificando URI)
RUTA_LIMPIA=\$(echo "\$NAUTILUS_SCRIPT_CURRENT_URI" | sed 's|^file://||' | sed 's|%20| |g')

# Moverse a esa carpeta y ejecutar el script
cd "\$RUTA_LIMPIA"

# Ejecutar en una nueva terminal (Kitty)
# Si no usas Kitty, cambia "kitty" por "gnome-terminal" o "xterm"
kitty -- sh -c "/usr/bin/python \"$SCRIPT_DIR/main.py\" $COMANDO; echo; echo '--- Proceso terminado ---'; exec sh"
EOF

    chmod +x "$RUTA_DESTINO"
    echo "  ✅ Script '$NOMBRE' creado dentro de carpeta AutoCracker."
}

# 3. Crear los 5 scripts dentro de la carpeta
create_script "GSE" "gse"
create_script "SteamClient" "steamclient"
create_script "Unsteam" "unsteam"
create_script "Unsteam-WIMM" "unsteam-wimm"
create_script "Steamless" "steamless"

echo ""
echo "========================================================"
echo "✅ Instalación completada."
echo "   Ve a una carpeta de un juego -> Click derecho -> Scripts -> AutoCracker -> [Opción]"
echo "========================================================"