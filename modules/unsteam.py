import os
import shutil
from tools import tools

def apply(config, resultados, directorio_ejecucion, APPID, wimm=False):
    unsteam_config = config.get("Unsteam", {})
    
    # 1. Seleccionar el .exe del juego
    selectExe = tools.seleccionar_archivo(resultados, directorio_ejecucion)
    if not selectExe:
        return False

    relativeExe = os.path.relpath(selectExe, directorio_ejecucion)
    
    # 2. Detectar arquitectura y definir rutas base
    arquitectura = tools.comprobar_arquitectura(selectExe)
    print(f"Arquitectura detectada: {arquitectura}")
    
    if arquitectura == "x86":
        RUTA_UNSTEAM_BASE = unsteam_config.get("x86", "")
    elif arquitectura == "x64":
        RUTA_UNSTEAM_BASE = unsteam_config.get("x64", "")
    else:
        print(f"Arquitectura no soportada para Unsteam: {arquitectura}")
        return False
    
    RUTA_WIMM = unsteam_config.get("wimm", "")

    print(f"\n📂 Copiando archivos Unsteam a: {directorio_ejecucion}")

    # 3. Lógica de copiado
    if wimm:
        # ============================================================
        # MODO UNSTEAM-WIMM (Solo copia archivos específicos)
        # ============================================================
        archivos_a_copiar = ["unsteam.dll", "unsteam.ini"]
        
        print("🔹 Modo WIMM activado (copiado selectivo).")
        
        # a) Copiar unsteam.dll y unsteam.ini
        for archivo in archivos_a_copiar:
            origen = os.path.join(RUTA_UNSTEAM_BASE, archivo)
            destino = os.path.join(directorio_ejecucion, archivo)
            
            if os.path.exists(origen):
                shutil.copy2(origen, destino)
                print(f"  ✅ {archivo} copiado.")
            else:
                print(f"  ⚠️ Advertencia: '{archivo}' no encontrado en {RUTA_UNSTEAM_BASE}.")

        # b) Copiar todo el contenido de la carpeta wimm
        print(f"\n📂 Copiando contenido de WIMM desde: {RUTA_WIMM}")
        if not os.path.exists(RUTA_WIMM):
            print(f"  ⚠️ Advertencia: La carpeta WIMM no existe en {RUTA_WIMM}.")
        else:
            for item in os.listdir(RUTA_WIMM):
                origen = os.path.join(RUTA_WIMM, item)
                destino = os.path.join(directorio_ejecucion, item)
                
                try:
                    if os.path.isdir(origen):
                        if os.path.exists(destino):
                            shutil.rmtree(destino)
                        shutil.copytree(origen, destino)
                        print(f"  ✅ Carpeta '{item}' copiada.")
                    else:
                        shutil.copy2(origen, destino)
                        print(f"  ✅ Archivo '{item}' copiado.")
                except Exception as e:
                    print(f"  ⚠️ Error copiando '{item}': {e}")

    else:
        # ============================================================
        # MODO UNSTEAM NORMAL (Copia todo el contenido)
        # ============================================================
        print("🔹 Modo Normal (copiado completo de la carpeta Release).")
        
        # Copiar todo el contenido de la carpeta de Release al directorio del juego
        if os.path.exists(RUTA_UNSTEAM_BASE):
            for item in os.listdir(RUTA_UNSTEAM_BASE):
                origen = os.path.join(RUTA_UNSTEAM_BASE, item)
                destino = os.path.join(directorio_ejecucion, item)
                
                try:
                    if os.path.isdir(origen):
                        if os.path.exists(destino):
                            shutil.rmtree(destino)
                        shutil.copytree(origen, destino)
                        print(f"  ✅ Carpeta '{item}' copiada.")
                    else:
                        shutil.copy2(origen, destino)
                        print(f"  ✅ Archivo '{item}' copiado.")
                except Exception as e:
                    print(f"  ⚠️ Error copiando '{item}': {e}")
        else:
            print(f"  ❌ Error: La carpeta de Unsteam no existe: {RUTA_UNSTEAM_BASE}")
            return False

    # ============================================================
    # 4. Modificar el archivo .ini
    # ============================================================
    
    print("\n" + "="*50)
    tools.modificar_ini_config(
        directorio_juego=directorio_ejecucion,
        nuevo_exe=relativeExe,
        nuevo_appid=APPID,
        nombre_ini_preferido="unsteam.ini"
    )
    print("="*50)
    
    return True