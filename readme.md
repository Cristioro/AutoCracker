# AutoCracker Steam (Multi-Tool)

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey)

Una herramienta todo-en-uno en Python para desempaquetar, parchear y aplicar cracks a juegos de Steam. Compatible con **Goldberg Steam Emulator (GSE)**, **ColdClientLoader**, **Unsteam** y **Steamless**, con soporte nativo para Linux (vía Wine).

---

## ✨ Características

*   **Múltiples motores de crack:** GSE (Goldberg), SteamClient (ColdClientLoader), Unsteam y Steamless.
*   **Detección automática de arquitectura:** Detecta automáticamente si el ejecutable del juego es `x86` o `x64`.
*   **Selección interactiva:** Si hay varios `.exe` en la carpeta, te permite elegir cuál modificar.
*   **Soporte multiplataforma:** Funciona tanto en Windows como en Linux (utiliza Wine para las herramientas de Windows).
*   **Configuración centralizada:** Todos los paths se manejan desde un `config.json` fácil de editar.
*   **Copia inteligente de archivos:** Copia archivos específicos o carpetas completas según el modo seleccionado (especialmente útil para `Unsteam-WIMM`).
*   **Modificación automática de INI:** Edita automáticamente los archivos `ColdClientLoader.ini` y `unsteam.ini` para reemplazar el nombre del ejecutable y el APPID.
*   **Desempaquetado automático (Steamless):** Ejecuta Steamless, renombra el original a `.bak` y deja el juego listo con el ejecutable desempaquetado.

---

## 📂 Estructura del proyecto

```text
AutoCracker/
├── main.py                     # Punto de entrada principal
├── config.json                 # Configuración de rutas de Assets
├── credentials.json            # Credenciales de GSE (Usuario/Contraseña)
├── modules/                    # Módulos de cada motor de crack
│   ├── gse.py
│   ├── steamclient.py
│   ├── unsteam.py
│   └── steamless.py
├── tools/                      # Herramientas auxiliares
│   ├── tools.py                # (Selección, arq. PE, modificación INI)
│   └── __init__.py
├── search.py                   # Lógica de búsqueda de archivos
```

---

## 🔧 Requisitos previos

*   **Python 3.8+** instalado.
*   **En Linux:** `wine` y `winetricks` instalados.
    *   `sudo apt install wine winetricks` (o el gestor de paquetes de tu distro).

---

## ⚙️ Configuración inicial

### 1. Configurar `config.json`
Abre el archivo `config.json` y asegúrate de que las rutas apunten correctamente a las carpetas de los motores:

```json
{
    "GSE": {
        "win" : "./Assets/GSE/GSE_Win",
        "linux" : "./Assets/GSE/GSE_Linux",
        "Gen_win" : "./Assets/GSE/gen_emu_config_old-win",
        "Gen_linux" : "./Assets/GSE/gen_emu_config_old-linux",
        "steamSettings" : "./Assets/GSE/steam_settings"
    },
    "Unsteam": {
        "x64": "./Assets/Unsteam/Unsteam_x64_Release",
        "x86": "./Assets/Unsteam/Unsteam_x86_Release",
        "wimm": "./Assets/Unsteam/wimm"
    },
    "Steamless": "./Assets/Steamless"
}
```
*(Las rutas relativas `./` son relativas a donde se encuentra el archivo `main.py`).*

### 2. Configurar `credentials.json` (Para GSE/SteamClient)
Crea un archivo llamado `credentials.json` en la raíz con este formato:
```json
{
    "GSE_USERNAME": "tu_usuario",
    "GSE_PASSWORD": "tu_contraseña"
}
```

### 3. Coloca los Assets
Descarga los binarios de los motores y colócalos en las carpetas correspondientes dentro de `Assets/`. 
*(Ejemplo: Steamless.exe dentro de `Assets/Steamless/`)*.

---

## 🚀 Cómo usar

Navega a la **carpeta raíz de tu juego** en la terminal y ejecuta el script con Python.

```bash
cd /ruta/de/tu/juego
python /ruta/hacia/AutoCracker/main.py [COMANDO] [APPID] #opcional
```

### 📋 Lista de comandos disponibles

| Comando | Descripción | ¿Requiere APPID? |
| :--- | :--- | :--- |
| `gse` | Aplica el crack GSE clásico (modifica `steam_api*.dll`). | Sí |
| `steamclient` | Aplica ColdClientLoader. Copia dlls, `.ini` y el loader. | Sí |
| `unsteam` | Copia **todo** el contenido de la carpeta Release de Unsteam al juego. | Sí |
| `unsteam-wimm` | Copia solo `unsteam.dll`, `unsteam.ini` y **todo el contenido** de la carpeta `wimm`. | Sí |
| `steamless` | Desempaqueta el `.exe` del juego usando Steamless. | No |
| `dryrun` | Solo muestra los archivos que se encontrarán en la carpeta del juego y no realiza ninguna acción. | No |

#### Ejemplos de uso:
```bash
# Para GTA V o juegos con steam_api
python main.py gse

python main.py gse 730

# Para usar el ColdClientLoader (SteamClient)
python main.py steamclient 730

# Para Unsteam en juegos con APPID 480
python main.py unsteam 480

# Para utilizar la versión WIMM de Unsteam
python main.py unsteam-wimm 480

# Para desempaquetar un .exe (Steamless)
python main.py steamless

# Para ver los archivos que se encontrarán en la carpeta del juego
python main.py dryrun
```

---

## 🐧 Soporte en Linux

El script detecta automáticamente si estás en Linux y ejecuta las herramientas `.exe` a través de `wine`.

*   **Steamless:** Si ves un error relacionado con `.NET` al ejecutar Steamless, el script te recomendará ejecutar el siguiente comando para instalar el framework necesario:
    ```bash
    winetricks dotnet48
    ```

---

## ⚠️ Aviso Legal

Esta herramienta es únicamente para fines educativos y de investigación. El uso de cracks y emuladores en juegos comerciales puede infringir los términos de servicio del desarrollador. Por favor, utiliza esta herramienta de forma responsable y solo en juegos de tu propiedad.

