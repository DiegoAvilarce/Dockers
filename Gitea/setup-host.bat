@echo off
:: Script simple para configurar archivo hosts
:: Debe ejecutarse como Administrador

echo ================================================
echo        Configurador de Hosts Simple
echo ================================================
echo.

:: Verificar permisos de administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Debes ejecutar como Administrador
    pause
    exit /b 1
)

:: Solicitar datos
set /p IP_ADDRESS="Ingresa la IP: "
set /p HOST_NAME="Ingresa el nombre del host: "

:: Verificar que no estén vacíos
if "%IP_ADDRESS%"=="" (
    echo ERROR: La IP no puede estar vacía
    pause
    exit /b 1
)

if "%HOST_NAME%"=="" (
    echo ERROR: El nombre del host no puede estar vacío
    pause
    exit /b 1
)

echo.
echo Agregando: %IP_ADDRESS% %HOST_NAME%

:: Agregar al archivo hosts con salto de línea
echo. >> C:\Windows\System32\drivers\etc\hosts
echo %IP_ADDRESS% %HOST_NAME% >> C:\Windows\System32\drivers\etc\hosts

:: Verificar si se agregó correctamente
if %errorLevel% neq 0 (
    echo ERROR: No se pudo escribir en el archivo hosts
    pause
    exit /b 1
)

echo OK: Configuracion completada
echo.
echo Ahora puedes acceder a: http://%HOST_NAME%:3000
echo.
pause