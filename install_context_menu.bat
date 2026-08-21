@echo off
setlocal enabledelayedexpansion

:: Obtener la ruta donde está este .bat
set "SCRIPT_DIR=%~dp0"
:: Quitar la barra final
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

echo ========================================================
echo Instalando AutoCracker en el menu contextual de Windows...
echo ========================================================
echo.

:: 1. Crear la clave principal en el menú contextual de carpetas
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker" /ve /d "AutoCracker Steam" /f
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker" /v "Icon" /d "%SCRIPT_DIR%\main.py" /f
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker" /v "SubCommands" /d "" /f

:: 2. Crear las opciones dentro del submenú
:: Opción GSE
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker\shell\gse" /ve /d "Aplicar GSE (pedirá APPID)" /f
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker\shell\gse\command" /ve /d "cmd.exe /c \"cd /d \"%%V\" && python \"%SCRIPT_DIR%\main.py\" gse\"" /f

:: Opción SteamClient
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker\shell\steamclient" /ve /d "Aplicar SteamClient (GSE + ColdClient)" /f
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker\shell\steamclient\command" /ve /d "cmd.exe /c \"cd /d \"%%V\" && python \"%SCRIPT_DIR%\main.py\" steamclient\"" /f

:: Opción Unsteam
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker\shell\unsteam" /ve /d "Aplicar Unsteam (Normal)" /f
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker\shell\unsteam\command" /ve /d "cmd.exe /c \"cd /d \"%%V\" && python \"%SCRIPT_DIR%\main.py\" unsteam\"" /f

:: Opción Unsteam-WIMM
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker\shell\unsteam-wimm" /ve /d "Aplicar Unsteam (Con WIMM)" /f
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker\shell\unsteam-wimm\command" /ve /d "cmd.exe /c \"cd /d \"%%V\" && python \"%SCRIPT_DIR%\main.py\" unsteam-wimm\"" /f

:: Opción Steamless
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker\shell\steamless" /ve /d "Desempaquetar .exe con Steamless" /f
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker\shell\steamless\command" /ve /d "cmd.exe /c \"cd /d \"%%V\" && python \"%SCRIPT_DIR%\main.py\" steamless\"" /f

echo.
echo ========================================================
echo ✅ Instalacion completada.
echo    Ve a una carpeta de un juego, haz click derecho y busca "AutoCracker Steam".
echo ========================================================
pause