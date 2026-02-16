# 🛠️ Scripts de Ayuda - AI Agent Wizard

Esta carpeta contiene scripts utilitarios para facilitar el desarrollo y distribución del proyecto.

## 📤 Scripts de Git Push

Estos scripts automatizan el proceso de subir cambios a GitHub:

### Para Windows

- **[git_push.ps1](git_push.ps1)** - PowerShell (recomendado)
  ```powershell
  .\scripts\git_push.ps1
  ```

- **[git_push.bat](git_push.bat)** - CMD (alternativo)
  ```cmd
  scripts\git_push.bat
  ```

### Para Linux/macOS

- **[git_push.sh](git_push.sh)** - Bash
  ```bash
  chmod +x scripts/git_push.sh
  ./scripts/git_push.sh
  ```

## ⚙️ Configuración

- **[configure_online_installer.py](configure_online_installer.py)** - Configurador del instalador online
  ```bash
  python scripts/configure_online_installer.py usuario/repo [rama]
  ```
  
  Actualiza automáticamente `install_online.py` con la URL del repositorio.

- **[verify_compatibility.py](verify_compatibility.py)** - Verificador de compatibilidad
  ```bash
  python scripts/verify_compatibility.py
  ```
  
  Verifica que el proyecto sea compatible con Windows, Linux y macOS.

## 🚀 Uso desde la raíz del proyecto

Todos los scripts están diseñados para ejecutarse desde la raíz del proyecto:

```bash
# Desde la raíz
cd AI_AGENT_WIZARD

# Windows PowerShell
.\scripts\git_push.ps1

# Linux/macOS
./scripts/git_push.sh

# Configurar repositorio
python scripts/configure_online_installer.py simoncampos/ai_agent_wizard
```

## 📝 Qué hacen estos scripts

### git_push.*
1. Verifican que sea un repositorio git (inicializan si no lo es)
2. Agregan remote si no existe
3. Muestran archivos modificados
4. Agregan todos los cambios
5. Crean commit (mensaje personalizable)
6. Suben a GitHub (rama main)
7. Muestran URLs finales del instalador online

### configure_online_installer.py
1. Validan el formato del repositorio (owner/repo)
2. Actualizan `GITHUB_REPO` y `GITHUB_BRANCH` en `install_online.py`
3. Generan la URL de descarga para usuarios
4. Muestran comando de instalación final

## 🔒 Notas de Seguridad

- Los scripts no eliminan ni modifican archivos de código fuente
- Solo interactúan con git y archivos de configuración
- Piden confirmación antes de acciones importantes (en modo no automático)
- Son seguros para ejecutar múltiples veces

## 🐛 Troubleshooting

### "Permiso denegado" en Linux/macOS
```bash
chmod +x scripts/git_push.sh
```

### "Script deshabilitado" en Windows PowerShell
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "No se puede encontrar la ruta"
Asegúrate de estar en la raíz del proyecto:
```bash
cd /path/to/AI_AGENT_WIZARD
ls -l scripts/  # Debe listar los scripts
```
