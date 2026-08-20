import os
import fnmatch

# Blacklist global (puedes modificarla desde main.py)
BLACKLIST_DEFAULT = [
    "UnityCrashHandler64.exe",
    "UnityCrashHandler.exe"
]

def buscar_archivos(directorio, patrones, blacklist=None, excluir_blacklist=True):
    """
    Busca archivos que coincidan con los patrones
    
    Args:
        directorio: Directorio donde buscar
        patrones: Lista de patrones (ej: ["*.exe", "*.dll"])
        blacklist: Lista de nombres a excluir
        excluir_blacklist: Si es True, excluye los archivos de la blacklist
    """
    if blacklist is None:
        blacklist = BLACKLIST_DEFAULT
    
    resultados = []
    
    for raiz, directorios, archivos in os.walk(directorio):
        for archivo in archivos:
            # Verificar blacklist
            if excluir_blacklist and archivo in blacklist:
                continue
            
            # Verificar patrones
            for patron in patrones:
                if fnmatch.fnmatch(archivo.lower(), patron.lower()):
                    ruta_completa = os.path.join(raiz, archivo)
                    resultados.append(ruta_completa)
                    break
    
    return resultados