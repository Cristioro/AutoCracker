@echo off
:: El primer argumento (%1) es la ruta de la carpeta del juego
cd /d "%~1"

:: Ejecutar el script
python "%~dp0main.py" %2

echo.
echo Presiona cualquier tecla para cerrar...
pause > nul

:: (OPCIONAL) Si quieres que este archivo se borre a sí mismo al cerrar la ventana,
:: descomenta la siguiente línea quitándole el 'REM ':
:: del "%~f0"