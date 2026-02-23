# AI Agent Wizard 🧙‍♂️

**Sistema automatizado de indexación y documentación para proyectos de software**

Optimiza la interacción con agentes de IA reduciendo el consumo de tokens hasta en un 95% y eliminando la necesidad de navegar entre archivos. Proporciona acceso directo a funciones, clases y endpoints con números de línea exactos, permitiendo que Claude, GPT y otros asistentes encuentren código relevante sin leer archivos completos ni buscar manualmente.

## 🚀 Instalación Rápida

```bash
# Linux / macOS
curl -O https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py && python3 install_online.py --auto

# Windows PowerShell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py" -OutFile "install_online.py"; python install_online.py --auto
```

📚 Ver [docs/INSTALL_GUIDE.md](docs/INSTALL_GUIDE.md) para más opciones de instalación.

---

## 🎯 Características

- ✅ **Sin dependencias externas** - Solo Python 3.7+ stdlib
- 📊 **Indexación automática** - Escanea y mapea todo el código fuente
- 🎯 **Acceso directo** - Números de línea exactos para cada función/clase
- 🔍 **Detección inteligente** - Identifica lenguajes, frameworks y arquitectura
- 🚀 **Cero navegación** - Elimina búsqueda manual entre archivos
- 📝 **Documentación autogenerada** - Crea guías de convenciones y testing
- 🐛 **Registro de errores** - Mantiene historial de problemas y soluciones
- 🔄 **Actualización incremental** - Reescanea cambios sin reinstalar
- 🧠 **Auto-documentado** - El wizard se aplica a sí mismo su propio sistema

---

## 🚀 Instalación

### 📡 Método 1: Instalación Online (Recomendado)

Descarga e instala la última versión automáticamente desde GitHub:

```bash
# Descargar solo el instalador online
curl -O https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py

# O con wget
wget https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py

# Ejecutar instalación automática
python3 install_online.py --auto
```

**Ventajas**: Siempre obtienes la última versión, limpieza automática, un solo comando.

### 💾 Método 2: Instalación Local (desde repositorio clonado)

Si ya clonaste el repositorio:

```bash
# Instalación rápida en proyecto actual
python3 install_online.py --auto

# Con progreso detallado
python3 install_online.py --auto --verbose

# Modo interactivo
python3 install_online.py

# Ver opciones
python3 install_online.py --help
```

---

## 💡 Ejemplo de uso

**Escenario**: Un agente de IA necesita encontrar la función que valida emails.

### ❌ Sin AI Agent Wizard (método tradicional)
```
1. grep -r "validate.*email" .     → 50+ resultados en 20 archivos
2. Leer src/utils.py (500 líneas) → No está aquí
3. Leer src/validators.py (300 líneas) → Tampoco
4. Leer src/auth/validators.py (450 líneas) → ¡Encontrada en línea 234!
⏱️ Tiempo: 2-3 minutos | 📊 Tokens: ~8,000
```

### ✅ Con AI Agent Wizard
```
1. Abrir .ai/PROJECT_INDEX.yaml
2. Buscar "email" → src/auth/validators.py:validate_email (línea 234)
3. Leer líneas 234-245 directamente
⏱️ Tiempo: 10 segundos | 📊 Tokens: ~150 (95% reducción)
```

---

## 📁 Archivos generados

El wizard crea un sistema completo en la carpeta `.ai/`:

| Archivo | Descripción |
|---------|-------------|
| `PROJECT_INDEX.yaml` | 📚 Índice completo: archivos, funciones, endpoints, componentes |
| `CONVENTIONS.yaml` | 📐 Patrones de código y convenciones del proyecto |
| `TESTING.yaml` | 🧪 Comandos de validación y smoke tests |
| `ERRORS.yaml` | 🐛 Errores conocidos con soluciones documentadas |
| `GIT_WORKFLOW.yaml` | 🔀 Políticas de git, tipos de commits y versionado |
| `AGENT_GUIDE.md` | 🤖 Instrucciones para agentes de IA (Claude, Copilot, etc.) |
| `.cursorrules` | ⚙️ Symlink a AGENT_GUIDE.md para Cursor IDE |
| `update_index.py` | 🔄 Script para actualizar el índice después de cambios |

---

## 🏗️ Arquitectura

```
AI_AGENT_WIZARD/
├── src/                         # 📦 Código fuente
│   ├── core/                    # Lógica principal
│   │   ├── validators.py        # Validación de entorno (Python, Git, permisos)
│   │   ├── scanner.py           # Escaneo de archivos con progreso
│   │   ├── detectors.py         # Detección de lenguajes/frameworks
│   │   └── extractors.py        # Extracción de funciones/endpoints/componentes
│   ├── generators/              # Generación de contenido
│   │   └── all_generators.py   # Crea todos los archivos YAML
│   ├── templates/               # Templates de proyectos
│   │   └── project_templates.py # 12 tipos: Python/Flask/Django, Node, React, Vue...
│   ├── utils/                   # Utilidades
│   │   └── warnings.py          # Sistema de advertencias con modo verbose
│   └── main.py                  # Entry point principal
│
├── docs/                        # 📚 Documentación
│   ├── INSTALL_GUIDE.md         # Guía de instalación simplificada
│   ├── INSTALL_ONLINE.md        # Documentación técnica del instalador
│   ├── QUICKSTART_ONLINE.md     # Guía rápida de referencia
│   ├── AGENT_GUIDE.md                # Instrucciones para agentes de IA
│   ├── IMPLEMENTATION_SUMMARY.md # Resumen de implementación
│   └── READY_TO_PUSH.md         # Checklist de publicación
│
├── scripts/                     # 🛠️ Scripts de ayuda
│   ├── git_push.ps1             # Push automático (PowerShell)
│   ├── git_push.sh              # Push automático (Bash)
│   ├── git_push.bat             # Push automático (CMD)
│   └── configure_online_installer.py # Configurador del instalador
│
├── tests/                       # 🧪 Tests
│   └── test_all.py              # Tests unitarios (7 tests)
│
├── install_online.py            # 🌐 Instalador (online y local)
├── README.md                    # 📖 Este archivo
├── CHANGELOG.md                 # 📝 Historial de cambios (movido a docs/)
├── LICENSE                      # ⚖️ Licencia MIT
└── requirements.txt             # 📦 Dependencias (ninguna)
```

---

## 📊 Uso del índice

### Para agentes de IA

Los agentes deben **leer `.ai/PROJECT_INDEX.yaml` ANTES** de explorar el código:

```yaml
# Ejemplo de índice generado
archivos:
  src/main.py:
    lineas: 215
    funciones:
      - install (línea 45)
      - validate_environment (línea 180)
    dependencias:
      - core.validators
      - generators.all_generators
```

**Beneficios clave**:
- ✅ **Acceso directo**: Saltar a `main.py:45` sin abrir/buscar archivos
- ✅ **Sin navegación**: No revisar 10 archivos para encontrar una función
- ✅ **Menos tokens**: Leer solo líneas 45-60 en vez de 215 líneas completas
- ✅ **Búsqueda instantánea**: `Ctrl+F` en YAML vs `grep` en toda la carpeta

### Actualizar después de cambios

```bash
python3 .ai/update_index.py
```

Esto reescanea el proyecto y actualiza `PROJECT_INDEX.yaml` sin reinstalar todo.

---

## 🧪 Testing

Ejecutar todos los tests:

```bash
python3 tests/test_all.py
```

Tests incluidos:
- ✅ Validación de Python 3.7+
- ✅ Detección de Git
- ✅ Escaneo de archivos
- ✅ Detección de lenguajes
- ✅ Extracción de funciones
- ✅ Sugerencia de templates

---

## 🛠️ Comandos útiles

```bash
# Validar sintaxis Python
find src -name "*.py" -exec python3 -m py_compile {} \;

# Ver estructura del proyecto
tree -L 3 -I '__pycache__|*.pyc'

# Contar líneas de código
find src -name "*.py" -exec wc -l {} + | tail -1

# Buscar TODOs pendientes
grep -r "# TODO" src/
```

---

## 🧩 Templates soportados

El wizard detecta automáticamente el mejor template según el stack:

- `python_script` - Scripts Python simples
- `python_flask` - Apps Flask
- `python_django` - Apps Django
- `python_fastapi` - APIs FastAPI
- `node_express` - APIs Express
- `react` - Apps React
- `vue` - Apps Vue 3
- `go` - Proyectos Go
- `rust` - Proyectos Rust
- `java` - Proyectos Java/Maven
- `generic` - Otros lenguajes

---

## 📦 Detección automática

### Lenguajes
Python, JavaScript, TypeScript, Go, Rust, Java, PHP, C#, Ruby, C, C++

### Frameworks detectados

**Backend:**
- Flask (app.py + requirements.txt con flask)
- Django (settings.py + manage.py)
- FastAPI (main.py + fastapi en deps)
- Express (package.json + express)

**Frontend:**
- Vue 3 (package.json + vue + vite.config)
- React (package.json + react)
- Angular (angular.json + @angular/core)

**Monorepos:**
- Lerna (lerna.json)
- pnpm (pnpm-workspace.yaml)
- Nx (nx.json)
- Turborepo (turbo.json)

---

## 🌐 Configuración del Instalador Online

El archivo [install_online.py](install_online.py) permite instalación remota desde GitHub.

### ⚙️ Configurar el repositorio (solo una vez)

Editar `install_online.py` líneas 28-29:

```python
GITHUB_REPO = "tu-usuario/ai-agent-wizard"  # Cambiar esto
GITHUB_BRANCH = "main"                       # O "master", etc.
```

### 📤 Distribuir a usuarios

Una vez configurado, los usuarios solo necesitan:

```bash
# Un solo comando (requiere curl)
curl -O https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py && python3 install_online.py --auto
```

O en dos pasos:

```bash
# 1. Descargar instalador
curl -O https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py

# 2. Ejecutar (instala, descarga código, limpia temporales)
python3 install_online.py --auto
```

### 💡 Ventajas del instalador online

- ✅ **1 archivo**: Solo 12 KB vs 300 KB del repo completo
- ✅ **Siempre actualizado**: Descarga última versión automáticamente
- ✅ **Auto-limpieza**: Borra archivos temporales al terminar
- ✅ **Sin Git**: No requiere tener Git instalado

Ver [docs/INSTALL_ONLINE.md](docs/INSTALL_ONLINE.md) para documentación técnica completa.

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit con Conventional Commits (`feat: nueva detección`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

---

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE)

---

## 🙏 Créditos

Desarrollado como herramienta de optimización para interacción con Claude Sonnet 4.5, GPT-4 y otros agentes de IA.

**Versión:** 2.1.0  
**Generado por:** AI Agent Wizard
