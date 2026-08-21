import os
import shutil
import subprocess

# Variables globales
Steam_api = None
steam_api_path = None

def apply(config, resultados):
    """Aplica el crack GSE"""
    global Steam_api, steam_api_path, ruta_backup  # ← DECLARAR GLOBAL
    
    # Cargar variables
    gse_config = config.get("GSE", {})
    GSE_WIN = gse_config.get("win", "")
    GSE_LINUX = gse_config.get("linux", "")
    
    # Buscar steam_api
    nombreApi = None
    Steam_api = None
    for ruta in resultados:
        print(ruta)
        nombreApi = os.path.basename(ruta)
        if nombreApi in ["steam_api64.dll", "steam_api.dll"]:
            Steam_api = ruta  # Global
            break
    
    if not Steam_api:
        print("No se encontró steam_api, no se puede continuar")
        return False
    
    steam_api_path = os.path.dirname(Steam_api) # Global
    print(f"Steam API encontrado: {Steam_api}")
    
    # Backup del original
    ruta_backup = os.path.join(steam_api_path, f"{nombreApi}.bak") # Global
    if os.path.exists(ruta_backup):
        os.remove(ruta_backup)
    os.rename(Steam_api, ruta_backup)
    print(f"{nombreApi} → {nombreApi}.bak")
    
    # Copiar archivos crack
    if nombreApi == "steam_api64.dll":
        origen_api = os.path.join(GSE_WIN, "experimental", "x64", "steam_api64.dll")
        origen_client = os.path.join(GSE_WIN, "experimental", "x64", "steamclient64.dll")
        destino_api = os.path.join(steam_api_path, "steam_api64.dll")
        destino_client = os.path.join(steam_api_path, "steamclient64.dll")
    else:
        origen_api = os.path.join(GSE_WIN, "experimental", "x32", "steam_api.dll")
        origen_client = os.path.join(GSE_WIN, "experimental", "x32", "steamclient.dll")
        destino_api = os.path.join(steam_api_path, "steam_api.dll")
        destino_client = os.path.join(steam_api_path, "steamclient.dll")
    
    if os.path.exists(origen_api):
        shutil.copy2(origen_api, destino_api)
        print(f"{os.path.basename(origen_api)} copiado")
    else:
        print(f"No encontrado: {origen_api}")
    
    if os.path.exists(origen_client):
        shutil.copy2(origen_client, destino_client)
        print(f"{os.path.basename(origen_client)} copiado")
    else:
        print(f"No encontrado: {origen_client}")
    
    return True

def generate_interfaces(config, directorio_ejecucion, sistema_operativo):
    """Genera steam_interfaces.txt"""
    global Steam_api, ruta_backup  # ← Necesitas la global
    
    if not Steam_api:
        print("Steam_api no encontrado, no se puede generar interfaces")
        return None
    
    gse_config = config.get("GSE", {})
    GSE_WIN = gse_config.get("win", "")
    GSE_LINUX = gse_config.get("linux", "")
    
    # Obtener nombre del archivo desde Steam_api
    nombre_api = os.path.basename(Steam_api)
    
    # Cargar herramienta según SO y arquitectura
    if sistema_operativo == "Windows":
        if nombre_api == "steam_api64.dll":
            generate_interfaces_exe = os.path.join(GSE_WIN, "tools", "generate_interfaces", "generate_interfaces_x64.exe")
        else:
            generate_interfaces_exe = os.path.join(GSE_WIN, "tools", "generate_interfaces", "generate_interfaces_x86.exe")
    else:  # Linux
        if nombre_api == "steam_api64.dll":
            generate_interfaces_exe = os.path.join(GSE_LINUX, "tools", "generate_interfaces", "generate_interfaces_x64")
        else:
            generate_interfaces_exe = os.path.join(GSE_LINUX, "tools", "generate_interfaces", "generate_interfaces_x86")
    
    print(f"Generando interfaces para: {nombre_api}")
    
    if not os.path.exists(generate_interfaces_exe):
        print(f"{generate_interfaces_exe} no encontrado")
        return None
    
    try:
        resultado = subprocess.run(
            [generate_interfaces_exe, ruta_backup],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if resultado.stdout:
            print(f"{resultado.stdout.strip()}")
        
        if resultado.stderr:
            print(f"Errores: {resultado.stderr.strip()}")
        
        # Verificar que se generó el archivo
        steam_interfaces_path = os.path.join(directorio_ejecucion, "steam_interfaces.txt")
        if os.path.exists(steam_interfaces_path):
            print(f"steam_interfaces.txt generado")
            return steam_interfaces_path
        else:
            print("No se generó steam_interfaces.txt")
            return None
            
    except subprocess.TimeoutExpired:
        print(f"Timeout generando interfaces para {Steam_api}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def generate_emu_config(config, credenciales, directorio_ejecucion, sistema_operativo, APPID, steamclient=False):
    """Genera configuración con generate_emu_config"""
    global steam_api_path  # ← Necesitas la global
    
    gse_config = config.get("GSE", {})
    GEN_WIN = gse_config.get("Gen_win", "")
    GEN_LINUX = gse_config.get("Gen_linux", "")
    CUSTOM_STEAM_SETTINGS = gse_config.get("steamSettings", "")
    
    # Cargar herramienta según SO
    if sistema_operativo == "Windows":
        generate_emu_config_exe = os.path.join(GEN_WIN, "generate_emu_config", "generate_emu_config.exe")
    else:
        generate_emu_config_exe = os.path.join(GEN_LINUX, "generate_emu_config", "generate_emu_config")
    
    if not os.path.exists(generate_emu_config_exe):
        print(f"generate_emu_config no encontrado: {generate_emu_config_exe}")
        return False
    
    # Generar archivo de configuración
    env = os.environ.copy()
    env['GSE_CFG_USERNAME'] = credenciales.get("GSE_USERNAME", "")
    env['GSE_CFG_PASSWORD'] = credenciales.get("GSE_PASSWORD", "")
    
    print(f"Generando configuración para APPID: {APPID}")
    print(f"   Usuario: {env['GSE_CFG_USERNAME']}")
    
    steamStettings_temp_path = None
    
    try:
        resultado = subprocess.run(
            [generate_emu_config_exe, "-clean", "-cve", "-reldir", APPID],
            env=env,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if resultado.returncode == 0:
            print("Configuración generada con éxito")
            if resultado.stdout:
                steamStettings_temp_path = os.path.join(directorio_ejecucion, "output", APPID, "steam_settings")
                print(f"steam_settings generado en: {steamStettings_temp_path}")
                print(f"\nSalida:\n{resultado.stdout}")
        else:
            print(f"Error (código {resultado.returncode})")
            if resultado.stderr:
                print(f"{resultado.stderr.strip()}")
            if resultado.stdout:
                print(f"{resultado.stdout.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print("Timeout: La operación tomó demasiado tiempo (>60 segundos)")
        return False
    except PermissionError:
        print(f"Permiso denegado para ejecutar: {generate_emu_config_exe}")
        print("   Asegúrate de que el archivo tiene permisos de ejecución")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        print(f"   Tipo de error: {type(e).__name__}")
        return False
    
    # Mover carpetas y archivos
    if steamStettings_temp_path and os.path.exists(steamStettings_temp_path):
        # Generar interfaces
        steam_interfaces_path = generate_interfaces(config, directorio_ejecucion, sistema_operativo)
        
        if steam_interfaces_path and os.path.exists(steam_interfaces_path):
            shutil.move(steam_interfaces_path, steamStettings_temp_path)
            print(f"steam_interfaces.txt movido a {steamStettings_temp_path}")
        
        # Copiar steam_settings personalizado
        if CUSTOM_STEAM_SETTINGS and os.path.exists(CUSTOM_STEAM_SETTINGS):
            shutil.copytree(CUSTOM_STEAM_SETTINGS, steamStettings_temp_path, dirs_exist_ok=True)
            print(f"steam_settings personalizado combinado")
        
        # Mover steam_settings al destino final
        if steamclient:
            # Modo steamclient: steam_settings en directorio de ejecución
            steamSettings_path = os.path.join(directorio_ejecucion, "steam_settings")
            if os.path.exists(steamSettings_path):
                shutil.rmtree(steamSettings_path)
            shutil.move(steamStettings_temp_path, steamSettings_path)
            print(f"steam_settings movido a {steamSettings_path}")
        else:
            # Modo normal: steam_settings junto al steam_api
            if steam_api_path:
                steamSettings_path = os.path.join(steam_api_path, "steam_settings")
                if os.path.exists(steamSettings_path):
                    shutil.rmtree(steamSettings_path)
                shutil.move(steamStettings_temp_path, steamSettings_path)
                print(f"steam_settings movido a {steamSettings_path}")
            else:
                print("steam_api_path no definido, no se puede mover steam_settings")
                return False
        
        # Limpiar temporales
        for carpeta in ["output", "backup"]:
            ruta = os.path.join(directorio_ejecucion, carpeta)
            if os.path.exists(ruta):
                shutil.rmtree(ruta)
                print(f"{carpeta} eliminado")
        
        return True
    
    print("No se generó steam_settings")
    return False