@echo off
title Instalador AutoSpicetify
color 0A

echo ===================================================
echo      INSTALADOR AUTOMATICO DO AUTO-SPICETIFY
echo ===================================================
echo.
echo 1. Identificando pasta de inicializacao...

set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

echo    Caminho: %STARTUP_FOLDER%
echo.

echo 2. Copiando executavel...

if not exist "AutoSpicetify.exe" (
    color 0C
    echo [ERRO] O arquivo AutoSpicetify.exe nao foi encontrado!
    echo Certifique-se de que este .bat esteja na mesma pasta do .exe.
    pause
    exit
)

copy /Y "AutoSpicetify.exe" "%STARTUP_FOLDER%\"

if %errorlevel% neq 0 (
    color 0C
    echo [ERRO] Falha ao copiar o arquivo.
    pause
    exit
)

echo.
echo 3. Executando pela primeira vez para configurar...
echo.

start "" "%STARTUP_FOLDER%\AutoSpicetify.exe"

echo ===================================================
echo [SUCESSO] Instalacao concluida! 
echo O programa rodara automaticamente ao ligar o PC.
echo ===================================================
timeout /t 5