import os
import subprocess
import platform
from tools import tools

def apply(config, resultados, directorio_ejecucion, sistema_operativo):
    # 1. Obtener la ruta de Steamless desde la configuración
    STEAMLESS_PATH = config.get("Steamless", "")
    
    if not STEAMLESS_PATH or not os.path.exists(STEAMLESS_PATH):
        print(f"❌ Error: No se encontró la carpeta de Steamless en: {STEAMLESS_PATH}")
        print("   Revisa tu config.json.")
        return False

    # 2. Seleccionar el .exe del juego
    selectExe = tools.seleccionar_archivo(resultados, directorio_ejecucion)
    if not selectExe:
        return False
    
    # 3. Detectar sistema operativo (ya viene por argumento)
    
    # 4. Construir la ruta del ejecutable de Steamless
    steamless_exe = os.path.join(STEAMLESS_PATH, "Steamless.CLI.exe")
    
    if not os.path.exists(steamless_exe):
        # Intentar buscar otro nombre común si falla
        steamless_exe = os.path.join(STEAMLESS_PATH, "Steamless.exe")
        if not os.path.exists(steamless_exe):
            print(f"❌ Error: No se encontró steamless-cli.exe ni Steamless.exe en: {STEAMLESS_PATH}")
            return False

    # 5. Preparar el comando
    comando_base = [steamless_exe, selectExe]

    print(f"\n🔹 Desempaquetando con Steamless...")
    print(f"   Archivo: {os.path.basename(selectExe)}")

    try:
        if sistema_operativo == "Windows":
            # MODO WINDOWS: Ejecutar directamente
            print("   Sistema: Windows (ejecución directa)")
            
            resultado = subprocess.run(
                comando_base,
                capture_output=True,
                text=True,
                timeout=120
            )
            
        elif sistema_operativo == "Linux":
            # MODO LINUX: Ejecutar con wine
            print("   Sistema: Linux (ejecutando con wine)")
            
            try:
                subprocess.run(["wine", "--version"], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("❌ Error: 'wine' no está instalado")
                print("   Instálalo con: sudo apt install wine (o el gestor de tu distro)")
                return False
            
            comando_wine = ["wine"] + comando_base
            resultado = subprocess.run(
                comando_wine,
                capture_output=True,
                text=True,
                timeout=120
            )
            
        else:
            print(f"❌ Sistema operativo no soportado: {sistema_operativo}")
            return False

        # 6. Verificar resultado
        if resultado.returncode == 0:
            print("✅ Steamless completado con éxito.")
            
            if resultado.stdout:
                print(f"\nSalida:\n{resultado.stdout.strip()}")
            
            # ================================================================
            # 🚀 BLOQUE DE RENOMBRADO DE ARCHIVOS
            # ================================================================
            directorio_juego = os.path.dirname(selectExe)
            nombre_original = os.path.basename(selectExe)
            nombre_sin_extension = os.path.splitext(nombre_original)[0]
            
            # Posibles nombres que genera Steamless
            posibles_outputs = [
                os.path.join(directorio_juego, f"{nombre_sin_extension}_unpacked.exe"),
                os.path.join(directorio_juego, f"{nombre_sin_extension}_unpacked (1).exe"),
                os.path.join(directorio_juego, f"{nombre_original}.unpacked.exe")
            ]
            
            archivo_desempaquetado = None
            for output in posibles_outputs:
                if os.path.exists(output):
                    archivo_desempaquetado = output
                    break
            
            if archivo_desempaquetado:
                print(f"\n📁 Archivo desempaquetado encontrado: {os.path.basename(archivo_desempaquetado)}")
                
                # PASO 1: Renombrar el original a .bak
                ruta_backup = os.path.join(directorio_juego, f"{nombre_original}.bak")
                if os.path.exists(selectExe):
                    if os.path.exists(ruta_backup):
                        os.remove(ruta_backup)
                    os.rename(selectExe, ruta_backup)
                    print(f"  🔄 Original renombrado a: {os.path.basename(ruta_backup)}")
                
                # PASO 2: Renombrar el desempaquetado al nombre original
                if os.path.exists(ruta_backup) and os.path.exists(archivo_desempaquetado):
                    # Si por alguna razón el archivo original sigue existiendo, lo borramos para sobrescribir
                    if os.path.exists(selectExe):
                        os.remove(selectExe)
                    
                    os.rename(archivo_desempaquetado, selectExe)
                    print(f"  🎯 Desempaquetado renombrado a: {nombre_original}")
                    print("  ✅ El juego ahora usará el ejecutable desempaquetado.")
            else:
                print("⚠️ No se encontró el archivo desempaquetado generado por Steamless.")
            
            return True
            
        else:
            print(f"❌ Error en Steamless (código {resultado.returncode})")
            
            if resultado.stderr:
                stderr_lower = resultado.stderr.lower()
                print(f"\nError detectado:\n{resultado.stderr.strip()}")
                
                # Si es Linux y hay error de .NET, sugerir winetricks
                if sistema_operativo == "Linux" and ("dotnet" in stderr_lower or "framework" in stderr_lower):
                    print("\n" + "="*60)
                    print("⚠️  PARECE QUE FALTA .NET FRAMEWORK EN WINE")
                    print("="*60)
                    print("Para solucionarlo, ejecuta el siguiente comando en tu terminal:")
                    print("  winetricks dotnet48")
                    print("\n(Opcionalmente, también puedes necesitar: winetricks corefonts)")
                    print("="*60)
                    
            return False

    except subprocess.TimeoutExpired:
        print("❌ Error: La operación de Steamless excedió el tiempo límite (120 segundos).")
        return False
    except FileNotFoundError:
        print(f"❌ Error: No se pudo ejecutar '{steamless_exe}'. ¿El archivo existe y tiene permisos?")
        return False
    except Exception as e:
        print(f"❌ Error inesperado ejecutando Steamless: {e}")
        return False