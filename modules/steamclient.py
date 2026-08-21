import os
import shutil
from tools import tools

def apply(config, resultados, directorio_ejecucion, APPID):
    # Cargar variables
    gse_config = config.get("GSE", {})
    GSE_WIN = gse_config.get("win", "")
    
    # 1. seleccionar el archivo
    selectExe = tools.seleccionar_archivo(resultados, directorio_ejecucion)
    if not selectExe:
        return False
    relativeExe = os.path.relpath(selectExe, directorio_ejecucion)
    
    arquitectura = tools.comprobar_arquitectura(selectExe)
    print(f"Arquitectura detectada: {arquitectura}")

    # Definir la lista de archivos/carpetas a copiar
    copy_forever = [
        "extra_dlls/",  # Ruta de carpeta (termina en /)
        "ColdClientLoader.ini",
        "GameOverlayRenderer.dll",
        "GameOverlayRenderer64.dll",
        "steamclient.dll",
        "steamclient64.dll"
    ]
    origen_base = os.path.join(GSE_WIN, "steamclient_experimental")
    # 2. Determinar la ruta de origen de los archivos Steamclient según la arquitectura
    if arquitectura == "x86":
        SteamclientExe = os.path.join(GSE_WIN, "steamclient_experimental", "steamclient_loader_x86.exe")
    elif arquitectura == "x64":
        SteamclientExe = os.path.join(GSE_WIN, "steamclient_experimental", "steamclient_loader_x64.exe")
    else:
        print(f"Arquitectura no soportada para Steamclient: {arquitectura}")
        return False

    # 3. COPIAR TODO LO DE COPY_FOREVER AL DIRECTORIO DE EJECUCIÓN
    print(f"\nCopiando archivos de Steamclient a: {directorio_ejecucion}")
    
    for item in copy_forever:
        origen = os.path.join(origen_base, item)
        destino = os.path.join(directorio_ejecucion, item)
        
        # Comprobar si el archivo/carpeta existe en el origen
        if not os.path.exists(origen):
            print(f"  ⚠️ Advertencia: '{item}' no encontrado en {origen_base}. Se omite.")
            continue

        # Si es una carpeta (termina en /) o es un directorio
        if item.endswith("/") or os.path.isdir(origen):
            # Si ya existe la carpeta en el destino, la sobreescribimos
            if os.path.exists(destino):
                shutil.rmtree(destino)  # Borramos la antigua para evitar conflictos
            shutil.copytree(origen, destino)
            print(f"  ✅ Carpeta '{item}' copiada correctamente.")
        else:
            # Si es un archivo, lo copiamos
            shutil.copy2(origen, destino)
            print(f"  ✅ Archivo '{item}' copiado correctamente.")

    # 4. Copiar el ejecutable del loader (SteamclientExe) si existe
    if os.path.exists(SteamclientExe):
        shutil.copy2(SteamclientExe, os.path.join(directorio_ejecucion, os.path.basename(SteamclientExe)))
        print(f"  ✅ Loader copiado: {os.path.basename(SteamclientExe)}")
    else:
        print(f"  ⚠️ Advertencia: Loader no encontrado: {SteamclientExe}")

    print("=" * 50)
    print("Copiado completado.")

    tools.modificar_ini_config(directorio_ejecucion, nuevo_exe=relativeExe, nuevo_appid=APPID, nombre_ini_preferido="ColdClientLoader.ini")