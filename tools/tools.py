def comprobar_arquitectura(ruta_archivo):
    import struct
    try:
        with open(ruta_archivo, 'rb') as f:
            # Verifica que sea un archivo ejecutable válido (debe empezar con 'MZ')
            if f.read(2) != b'MZ':
                return "No es un archivo ejecutable (.exe) válido."
            
            # Busca la posición de la cabecera PE en el byte 0x3C
            f.seek(0x3C)
            pe_offset = struct.unpack('<I', f.read(4))[0]
            
            # Se mueve a la firma PE (le suma 4 bytes de la firma 'PE\0\0')
            f.seek(pe_offset + 4)
            
            # Lee el tipo de máquina (2 bytes)
            machine = struct.unpack('<H', f.read(2))[0]
            
            # Identifica la arquitectura según el código de la máquina
            if machine == 0x014c:
                return "x86"
            elif machine == 0x8664:
                return "x64"
            elif machine == 0xaa64:
                return "ARM64"
            else:
                return f"Arquitectura desconocida (Código: {hex(machine)})"
                
    except FileNotFoundError:
        return "Error: El archivo no fue encontrado."
    except Exception as e:
        return f"Ocurrió un error al leer el archivo: {e}"

def seleccionar_archivo(resultados, directorio_ejecucion):
    import os
    
    if not resultados:
        print("No se encontraron archivos.")
        return None

    # Mostrar separador y lista
    print(f"Se encontraron {len(resultados)} archivos:")
    for i, ruta in enumerate(resultados):
        # CORRECCIÓN: Usar 'ruta' (la variable del bucle), no resultados[0]
        relative_path = os.path.relpath(ruta, directorio_ejecucion)
        print(f"[{i+1}]. {relative_path}")

    # Lógica de selección
    if len(resultados) == 1:
        # Si solo hay 1, selecciona el primero automáticamente
        numberExe = 0
        print(f"\nSeleccionado automáticamente: {os.path.relpath(resultados[0], directorio_ejecucion)}")
    
    elif len(resultados) > 1:
        # Si hay más de 1, preguntar
        while True:
            seleccion = input("\nSelecciona un archivo (número): ").strip()
            
            if seleccion.isdigit():
                idx = int(seleccion) - 1  # Convertir a índice 0-based
                if 0 <= idx < len(resultados):
                    numberExe = idx
                    break
                else:
                    print(f"Error: Elige un número entre 1 y {len(resultados)}.")
            else:
                print("Error: Debes ingresar un número válido.")
    
    # Retornar la ruta COMPLETA (absoluta) del archivo seleccionado
    selectExe = resultados[numberExe]
    
    # Mostramos la ruta relativa en pantalla, pero retornamos la absoluta
    print(f"\nArchivo seleccionado: {os.path.relpath(selectExe, directorio_ejecucion)}")
    
    return selectExe

def modificar_ini_config(directorio_juego, nuevo_exe, nuevo_appid, nombre_ini_preferido=None):
    import os
    """
    Busca un archivo .ini (unsteam.ini o ColdClientLoader.ini) y modifica
    las variables del ejecutable y del AppID línea por línea.
    """
    
    posibles_nombres = ["unsteam.ini", "ColdClientLoader.ini"]
    if nombre_ini_preferido:
        posibles_nombres = [nombre_ini_preferido]

    ruta_ini = None
    
    # 1. Buscar el archivo .ini que exista
    for nombre in posibles_nombres:
        ruta_temp = os.path.join(directorio_juego, nombre)
        if os.path.exists(ruta_temp):
            ruta_ini = ruta_temp
            print(f"✅ Archivo .ini encontrado: {nombre}")
            break

    if not ruta_ini:
        print("❌ No se encontró ningún archivo .ini.")
        return False

    try:
        # 2. Leer todas las líneas del archivo
        with open(ruta_ini, 'r', encoding='utf-8') as f:
            lineas = f.readlines()

        # 3. Procesar línea por línea
        lineas_modificadas = []
        cambios_realizados = 0

        for linea in lineas:
            linea_original = linea
            
            # Buscar y reemplazar la línea del ejecutable
            # Usamos .lstrip() para ignorar espacios al principio de la línea
            if linea.lstrip().startswith(('Exe=', 'exe_file=')):
                # Reemplazamos lo que haya después del primer '='
                partes = linea.split('=', 1)
                linea = partes[0] + '=' + nuevo_exe + '\n'
                cambios_realizados += 1
                
            # Buscar y reemplazar la línea del AppID
            elif linea.lstrip().startswith(('AppId=', 'real_app_id=')):
                partes = linea.split('=', 1)
                linea = partes[0] + '=' + nuevo_appid + '\n'
                cambios_realizados += 1
            
            lineas_modificadas.append(linea)

        # 4. Si se hicieron cambios, guardar el archivo
        if cambios_realizados > 0:
            with open(ruta_ini, 'w', encoding='utf-8') as f:
                f.writelines(lineas_modificadas)
            
            print(f"✅ Archivo .ini modificado con éxito ({cambios_realizados} cambios).")
            print(f"   - Variable Ejecutable → '{nuevo_exe}'")
            print(f"   - Variable AppID → '{nuevo_appid}'")
            return True
        else:
            print("⚠️ No se encontraron las variables esperadas en el .ini.")
            print("   Buscaba líneas que empezaran con: Exe=, exe_file=, AppId=, o real_app_id=")
            return False

    except Exception as e:
        print(f"❌ Error al modificar el archivo .ini: {e}")
        return False