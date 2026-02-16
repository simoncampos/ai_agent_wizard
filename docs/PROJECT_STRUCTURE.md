# 📁 Estructura del Proyecto - AI Agent Wizard

## 🎯 Organización

Este proyecto mantiene una estructura organizada y limpia:

```
AI_AGENT_WIZARD/
│
├── 📦 src/                      # Código fuente del sistema
│   ├── core/                    # Lógica principal (validators, scanner, detectors, extractors)
│   ├── generators/              # Generación de YAML
│   ├── templates/               # Templates de proyectos
│   ├── utils/                   # Utilidades
│   └── main.py                  # Entry point
│
├── 📚 docs/                     # Toda la documentación
│   ├── README.md                # Índice de documentación
│   ├── INSTALL_GUIDE.md         # Guía de instalación simplificada
│   ├── INSTALL_ONLINE.md        # Documentación técnica
│   ├── QUICKSTART_ONLINE.md     # Referencia rápida
│   ├── CLAUDE.md                # Instrucciones para IA
│   ├── IMPLEMENTATION_SUMMARY.md # Resumen técnico
│   └── READY_TO_PUSH.md         # Checklist de publicación
│
├── 🛠️ scripts/                  # Scripts de ayuda
│   ├── README.md                # Documentación de scripts
│   ├── git_push.ps1             # PowerShell (Windows)
│   ├── git_push.sh              # Bash (Linux/macOS)
│   ├── git_push.bat             # CMD (Windows)
│   └── configure_online_installer.py # Configurador
│
├── 🧪 tests/                    # Tests unitarios
│   └── test_all.py              # 7 tests
│
├── 📖 README.md                 # Documentación principal
├── 📝 CHANGELOG.md              # Historial de cambios
├── ⚖️ LICENSE                   # MIT License
├── 💾 install.py                # Instalador local
├── 🌐 install_online.py         # Instalador online
├── 📦 requirements.txt          # Dependencias (ninguna)
└── 🚫 .gitignore                # Archivos ignorados
```

## 🎨 Principios de Organización

### ✅ Raíz Limpia
Solo archivos esenciales que todo proyecto debe tener en la raíz:
- Documentación principal (`README.md`)
- Licencia y changelog (`LICENSE`, `CHANGELOG.md`)
- Archivos de configuración (`.gitignore`, `requirements.txt`)
- Instaladores principales (`install.py`, `install_online.py`)

### 📁 Carpetas Especializadas
- **`src/`** - Todo el código fuente
- **`docs/`** - Toda la documentación
- **`scripts/`** - Scripts auxiliares y herramientas
- **`tests/`** - Tests unitarios

### 🔍 Fácil Navegación
- Cada carpeta tiene su propio `README.md`
- Nombres descriptivos y consistentes
- Estructura intuitiva y escalable

## 📚 Acceso Rápido a Documentación

| Necesitas... | Ve a... |
|-------------|---------|
| **Instalar el sistema** | [docs/INSTALL_GUIDE.md](docs/INSTALL_GUIDE.md) |
| **Documentación técnica** | [docs/INSTALL_ONLINE.md](docs/INSTALL_ONLINE.md) |
| **Referencia rápida** | [docs/QUICKSTART_ONLINE.md](docs/QUICKSTART_ONLINE.md) |
| **Guía para agentes IA** | [docs/CLAUDE.md](docs/CLAUDE.md) |
| **Subir a GitHub** | [docs/READY_TO_PUSH.md](docs/READY_TO_PUSH.md) |

## 🛠️ Scripts Disponibles

| Script | Plataforma | Uso |
|--------|-----------|-----|
| `scripts/git_push.ps1` | Windows PowerShell | `.\scripts\git_push.ps1` |
| `scripts/git_push.bat` | Windows CMD | `scripts\git_push.bat` |
| `scripts/git_push.sh` | Linux/macOS | `./scripts/git_push.sh` |
| `scripts/configure_online_installer.py` | Cross-platform | `python scripts/configure_online_installer.py owner/repo` |

## 🎯 Beneficios de Esta Estructura

✅ **Claridad** - Cada cosa en su lugar
✅ **Escalabilidad** - Fácil agregar nuevos documentos o scripts
✅ **Mantenibilidad** - Referencias claras entre archivos
✅ **Profesionalismo** - Estructura estándar de proyectos open source
✅ **Cross-platform** - Funciona igual en Windows, Linux y macOS

## 📝 Notas para Contribuidores

### Al agregar documentación
→ Ponla en `docs/` y actualiza `docs/README.md`

### Al agregar scripts
→ Ponlos en `scripts/` y actualiza `scripts/README.md`

### Al modificar código
→ Actualiza tests en `tests/` si es necesario

### Al cambiar instaladores
→ Actualiza documentación en `docs/INSTALL_*.md`

---

**Versión de estructura**: 1.1.0 (Reorganizada el 2026-02-16)
