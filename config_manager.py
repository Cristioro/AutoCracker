import os
import json

def load_config(archivo_config=None, base_dir=None):
    if archivo_config is None:
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        archivo_config = os.path.join(directorio_actual, "config.json")
    
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(archivo_config))
    
    try:
        with open(archivo_config, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        def resolver_paths(obj, base_dir):
            if isinstance(obj, dict):
                return {key: resolver_paths(value, base_dir) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [resolver_paths(item, base_dir) for item in obj]
            elif isinstance(obj, str):
                if obj.startswith('./'):
                    return os.path.normpath(os.path.join(base_dir, obj[2:]))
                elif not os.path.isabs(obj) and not obj.startswith(('.', '/', '~')):
                    return os.path.normpath(os.path.join(base_dir, obj))
                elif obj.startswith('~'):
                    return os.path.expanduser(obj)
                else:
                    return obj
            else:
                return obj
        
        config = resolver_paths(config, base_dir)
        return config
        
    except FileNotFoundError:
        print(f"Archivo {archivo_config} no encontrado.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error en el formato JSON: {e}")
        return {}

def load_credentials(archivo_credenciales=None, base_dir=None):
    if archivo_credenciales is None:
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        archivo_credenciales = os.path.join(directorio_actual, "credentials.json")
    
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(archivo_credenciales))
    
    try:
        with open(archivo_credenciales, 'r', encoding='utf-8') as f:
            credenciales = json.load(f)
        
        print(f"Credenciales cargadas: {credenciales.get('GSE_USERNAME', '')}")
        return credenciales
        
    except FileNotFoundError:
        print(f"credentials.json no encontrado.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error en el formato JSON: {e}")
        return {}