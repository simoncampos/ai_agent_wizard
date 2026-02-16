@echo off
REM Script batch para Windows CMD para subir a GitHub
REM Uso: git_push.bat

echo.
echo ========================================
echo   AI AGENT WIZARD - Git Push Helper
echo ========================================
echo.

REM Verificar si es un repositorio git
if not exist ".git" (
    echo ERROR: No es un repositorio git
    echo.
    echo Inicializando repositorio...
    git init
    echo Agregando remote...
    git remote add origin https://github.com/simoncampos/ai_agent_wizard.git
)

REM Verificar archivos modificados
echo Archivos modificados:
git status --short

REM Agregar todos los archivos
echo.
echo Agregando archivos...
git add .

REM Commit
echo.
set /p commit_msg="Mensaje del commit (Enter para usar por defecto): "
if "%commit_msg%"=="" (
    set commit_msg=feat: configurar instalador online con repo simoncampos/ai_agent_wizard
)
git commit -m "%commit_msg%"

REM Push
echo.
echo Subiendo a GitHub...
git branch -M main
git push -u origin main

echo.
echo ========================================
echo   SUBIDA COMPLETADA
echo ========================================
echo.

echo URL del instalador online:
echo https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py
echo.

echo Comando para usuarios:
echo curl -O https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py ^&^& python3 install_online.py --auto
echo.

pause
