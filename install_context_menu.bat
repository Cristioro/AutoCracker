@echo off
setlocal enabledelayedexpansion

echo ========================================================
echo Instalando AutoCracker en el menu contextual de Windows...
echo ========================================================
echo.

:: Obtener la ruta donde está este .bat
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

:: 1. Crear la clave principal en el menú contextual de carpetas
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker" /ve /d "AutoCracker Steam" /f
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker" /v "Icon" /d "%SCRIPT_DIR%\main.py" /f
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker" /v "SubCommands" /d "" /f

:: 2. Crear las opciones dentro del submenú
:: ESTO YA NO CREA NINGÚN TEMPORAL. Solo llama al lanzador.bat que tienes en tu carpeta.

:: Opción GSE
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker\shell\gse" /ve /d "Aplicar GSE (pedirá APPID)" /f
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker\shell\gse\command" /ve /d "cmd.exe /k \"\"%SCRIPT_DIR%\lanzador.bat\" \"%%V\" gse\"" /f

:: Opción SteamClient
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker\shell\steamclient" /ve /d "Aplicar SteamClient (GSE + ColdClient)" /f
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker\shell\steamclient\command" /ve /d "cmd.exe /k \"\"%SCRIPT_DIR%\lanzador.bat\" \"%%V\" steamclient\"" /f

:: Opción Unsteam
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker\shell\unsteam" /ve /d "Aplicar Unsteam (Normal)" /f
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker\shell\unsteam\command" /ve /d "cmd.exe /k \"\"%SCRIPT_DIR%\lanzador.bat\" \"%%V\" unsteam\"" /f

:: Opción Unsteam-WIMM
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker\shell\unsteam-wimm" /ve /d "Aplicar Unsteam (Con WIMM)" /f
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker\shell\unsteam-wimm\command" /ve /d "cmd.exe /k \"\"%SCRIPT_DIR%\lanzador.bat\" \"%%V\" unsteam-wimm\"" /f

:: Opción Steamless
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker\shell\steamless" /ve /d "Desempaquetar .exe con Steamless" /f
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker\shell\steamless\command" /ve /d "cmd.exe /k \"\"%SCRIPT_DIR%\lanzador.bat\" \"%%V\" steamless\"" /f

echo.
echo ========================================================
echo ✅ Instalacion completada con el metodo Lanzador (100% limpio).
echo    Ya no se generaran archivos temporales en la carpeta del juego.
echo ========================================================
pause