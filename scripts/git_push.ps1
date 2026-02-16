# Script de ayuda para subir el proyecto a GitHub
# Uso: .\git_push.ps1

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  AI AGENT WIZARD - Git Push Helper" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Verificar si es un repositorio git
if (-not (Test-Path ".git")) {
    Write-Host "ERROR: No es un repositorio git" -ForegroundColor Red
    Write-Host "`nInicializando repositorio..." -ForegroundColor Yellow
    git init
    Write-Host "Agregando remote..." -ForegroundColor Yellow
    git remote add origin https://github.com/simoncampos/ai_agent_wizard.git
}

# Verificar archivos modificados
Write-Host "Archivos modificados:" -ForegroundColor Green
git status --short

# Agregar todos los archivos
Write-Host "`nAgregando archivos..." -ForegroundColor Yellow
git add .

# Commit
Write-Host "`nCreando commit..." -ForegroundColor Yellow
$commitMsg = Read-Host "Mensaje del commit (Enter para usar por defecto)"
if ([string]::IsNullOrWhiteSpace($commitMsg)) {
    $commitMsg = "feat: configurar instalador online con repo simoncampos/ai_agent_wizard"
}
git commit -m $commitMsg

# Push
Write-Host "`nSubiendo a GitHub..." -ForegroundColor Yellow
git branch -M main
git push -u origin main

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  SUBIDA COMPLETADA" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

Write-Host "`nURL del instalador online:" -ForegroundColor Cyan
Write-Host "https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py" -ForegroundColor White

Write-Host "`nComando para usuarios:" -ForegroundColor Cyan
Write-Host "curl -O https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py && python3 install_online.py --auto`n" -ForegroundColor White
