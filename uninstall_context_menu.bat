@echo off
echo ========================================================
echo Eliminando AutoCracker del menu contextual de Windows...
echo ========================================================
echo.

reg delete "HKEY_CLASSES_ROOT\Directory\Background\shell\AutoCracker" /f >nul 2>&1

echo.
echo ========================================================
echo ✅ Desinstalacion completada. El menu ha sido eliminado.
echo ========================================================
pause