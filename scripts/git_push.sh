#!/bin/bash
#
# Script de ayuda para subir el proyecto a GitHub
# Uso: bash git_push.sh
#

echo ""
echo "========================================"
echo "  AI AGENT WIZARD - Git Push Helper"
echo "========================================"
echo ""

# Verificar si es un repositorio git
if [ ! -d ".git" ]; then
    echo "ERROR: No es un repositorio git"
    echo ""
    echo "Inicializando repositorio..."
    git init
    echo "Agregando remote..."
    git remote add origin https://github.com/simoncampos/ai_agent_wizard.git
fi

# Verificar archivos modificados
echo "Archivos modificados:"
git status --short

# Agregar todos los archivos
echo ""
echo "Agregando archivos..."
git add .

# Commit
echo ""
echo "Creando commit..."
read -p "Mensaje del commit (Enter para usar por defecto): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="feat: configurar instalador online con repo simoncampos/ai_agent_wizard"
fi
git commit -m "$commit_msg"

# Push
echo ""
echo "Subiendo a GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "========================================"
echo "  ✅ SUBIDA COMPLETADA"
echo "========================================"
echo ""

echo "URL del instalador online:"
echo "https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py"
echo ""

echo "Comando para usuarios:"
echo "curl -O https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py && python3 install_online.py --auto"
echo ""
