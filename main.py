import os
import sys
import json
import platform
from search import buscar_archivos
from config_manager import load_config, load_credentials

# Importar funciones de los modulos
from modules import gse
from modules import unsteam
from modules import steamclient
from modules import steamless

def main():
    if len(sys.argv) < 3:
        print("Uso: python main.py [gse|steamclient|unsteam|steamless] <APPID>")
        print("  gse         - aplicar solo GSE")
        print("  steamclient - aplicar GSE y steamclient")
        print("  unsteam     - aplicar unsteam")
        print("  steamless   - Desempaquetar .exe con Steamless")
        sys.exit(1)
    
    comando = sys.argv[1].lower()
    
    if comando not in ["gse", "steamclient", "unsteam", "steamless"]:
        print(f"Error: Comando '{comando}' no reconocido")
        sys.exit(1)
    
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    
    # ============================================================
    # CARGAR CONFIGURACION (usando tu config_manager.py)
    # ============================================================
    config_path = os.path.join(directorio_script, "config.json")
    config = load_config(config_path, base_dir=directorio_script)
    
    if not config:
        print("Error: No se pudo cargar config.json")
        sys.exit(1)
    
    # ============================================================
    # ACCEDER A LAS RUTAS (asi se usa con tu config_manager)
    # ============================================================
    
    # RUTAS GSE
    gse_config = config.get("GSE", {})
    GSE_WIN = gse_config.get("win", "")
    GSE_LINUX = gse_config.get("linux", "")
    GEN_WIN = gse_config.get("Gen_win", "")
    GEN_LINUX = gse_config.get("Gen_linux", "")
    STEAM_SETTINGS = gse_config.get("steamSettings", "")
    
    # RUTAS UNSTEAM
    unsteam_config = config.get("Unsteam", {})
    UNSTEAM_X64 = unsteam_config.get("x64", "")
    UNSTEAM_X86 = unsteam_config.get("x86", "")
    UNSTEAM_WIMM = unsteam_config.get("wimm", "")
    
    # RUTA STEAMLESS
    STEAMLESS_PATH = config.get("Steamless", "")
    
    # Mostrar rutas cargadas
    print("Configuracion cargada:")
    print(f"  GSE_WIN: {GSE_WIN}")
    print(f"  GSE_LINUX: {GSE_LINUX}")
    print(f"  GEN_WIN: {GEN_WIN}")
    print(f"  GEN_LINUX: {GEN_LINUX}")
    print(f"  STEAM_SETTINGS: {STEAM_SETTINGS}")
    print(f"  UNSTEAM_X64: {UNSTEAM_X64}")
    print(f"  UNSTEAM_X86: {UNSTEAM_X86}")
    print(f"  STEAMLESS: {STEAMLESS_PATH}")
    
    # ============================================================
    # CARGAR CREDENCIALES (solo si es necesario)
    # ============================================================
    credenciales = {}
    if comando in ["gse", "steamclient"]:
        credentials_path = os.path.join(directorio_script, "credentials.json")
        
        if not os.path.exists(credentials_path):
            print("Error: credentials.json no encontrado")
            print("Crea el archivo con:")
            print('{ "GSE_USERNAME": "tu_usuario", "GSE_PASSWORD": "tu_contraseña" }')
            sys.exit(1)
        
        credenciales = load_credentials(credentials_path, base_dir=directorio_script)
        
        if not credenciales.get("GSE_USERNAME") or not credenciales.get("GSE_PASSWORD"):
            print("Error: Credenciales incompletas en credentials.json")
            sys.exit(1)
        
        print(f"Usuario: {credenciales.get('GSE_USERNAME')}")
    
    # ============================================================
    # VARIABLES INICIALES
    # ============================================================
    directorio_ejecucion = os.getcwd()

    sistema_operativo = platform.system()

    # ============================================================
    # SOLICITAR APPID
    # ============================================================
    if len(sys.argv) > 2:
        # Si existe, lo tomamos y lo pasamos a minúsculas
        APPID = sys.argv[2].lower()
    else:
        # Si falta el segundo argumento, se lo pedimos al usuario
        APPID = input("Falta el segundo parámetro. Por favor, ingrésalo: ").lower()
    
    # ============================================================
    # EJECUTAR COMANDO
    # ============================================================
    print("\n" + "="*50)
    
    if comando == "gse":
        patrones = ["steam_api64.dll", "steam_api.dll"]
        resultados = buscar_archivos(directorio_ejecucion, patrones)
        gse.apply(config, resultados, directorio_ejecucion)
        gse.generate_emu_config(config, credenciales, directorio_ejecucion, sistema_operativo, APPID, steamclient=False)
    
    elif comando == "steamclient":
        print("⚠️ Módulo SteamClient en desarrollo")
        sys.exit(0)
    elif comando == "unsteam":
        print("⚠️ Módulo Unsteam en desarrollo")
        sys.exit(0)
    elif comando == "steamless":
        print("⚠️ Módulo Steamless en desarrollo")
        sys.exit(0)
    
    print("\n" + "="*50)
    print("Completado")

if __name__ == "__main__":
    main()