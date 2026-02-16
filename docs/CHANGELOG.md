# CHANGELOG

## [1.1.0] - 2026-02-16

### ✨ Nuevo: Instalador Online

#### 📡 install_online.py
- **Descarga automática**: Obtiene última versión desde GitHub
- **Sin Git requerido**: Usa urllib (stdlib) para descarga HTTP
- **Auto-limpieza**: Borra archivos temporales automáticamente
- **Cross-platform**: Funciona en Linux, macOS, Windows usando `os.path.join()`
- **Modos de operación**:
  * `--auto`: Instalación sin interacción
  * `--verbose`: Progreso detallado de descarga
  * Interactivo: Confirmación antes de instalar
- **Proceso**:
  1. Verifica conexión a internet
  2. Descarga ZIP del repositorio (< 500 KB)
  3. Extrae en directorio temporal
  4. Instala sistema .ai/
  5. Limpia todo rastro de archivos temporales
- **Seguridad**: Solo descarga desde GitHub oficial vía HTTPS
- **Tamaño**: 12 KB (vs 300 KB del repo completo)

### 📁 Reorganización del Proyecto

#### Nueva estructura de carpetas
- **docs/** - Toda la documentación organizada
  * `INSTALL_GUIDE.md` - Guía simplificada
  * `INSTALL_ONLINE.md` - Documentación técnica
  * `QUICKSTART_ONLINE.md` - Referencia rápida
  * `CLAUDE.md` - Instrucciones para IA
  * `IMPLEMENTATION_SUMMARY.md` - Resumen técnico
  * `READY_TO_PUSH.md` - Checklist de publicación
  
- **scripts/** - Scripts de ayuda organizados
  * `git_push.ps1` / `git_push.sh` / `git_push.bat` - Push automático
  * `configure_online_installer.py` - Configurador

#### Raíz limpia
Solo archivos esenciales en la raíz:
- `README.md`, `CHANGELOG.md`, `LICENSE`
- `install.py`, `install_online.py`
- `requirements.txt`, `.gitignore`
- Carpetas: `src/`, `tests/`, `docs/`, `scripts/`

#### 🛠️ configure_online_installer.py
- Script auxiliar para configurar `GITHUB_REPO`
- Actualizado para buscar `install_online.py` en raíz del proyecto
- Valida formato de repositorio (owner/repo)
- Genera URL de descarga para usuarios

#### 📚 INSTALL_ONLINE.md
- Documentación técnica completa del instalador online
- Diagrama de flujo del proceso
- Guía de troubleshooting
- Ejemplos de integración con NPM, Makefile
- Comparativa: Online vs Local

### 🎯 Mejoras de Documentación

#### README.md actualizado
- Nueva sección: "Método 1: Instalación Online (Recomendado)"
- Ejemplo comparativo: Con vs Sin AI Agent Wizard
- Beneficios cuantificados: 95% reducción tokens, 10s vs 2-3 min
- Comandos de un solo paso con curl/wget
- Énfasis en "cero navegación" y "acceso directo"

#### Propósito refinado
Ahora explícitamente menciona **dos objetivos principales**:
1. Reducción de tokens (hasta 95%)
2. Eliminación de navegación entre archivos

#### Archivos actualizados
- `src/main.py`: Banner "menos tokens, cero navegación"
- `src/generators/all_generators.py`: Headers de YAML más descriptivos
- `CLAUDE.md` generado: 4 beneficios listados explícitamente
- Mensajes de instalación: incluyen resumen de beneficios

### 🔧 Cambios Técnicos

- Banner de instalación más conciso y claro
- Resumen final muestra beneficios activos
- Mensajes de progreso optimizados
- Docstrings actualizados con propósito dual

---

## [1.0.0] - 2026-01-11

### ✨ Características implementadas

#### 🏗️ Arquitectura modular
- Separación en módulos: `core/`, `generators/`, `templates/`, `utils/`
- Imports absolutos desde `src/` base
- Estructura escalable y mantenible

#### 📊 Sistema de escaneo
- `scanner.py`: Escaneo de archivos fuente con exclusión de node_modules, venv, .git
- Contador de líneas y detector de tipos de archivo
- Barra de progreso integrada (ej: "19/19 (100%)")
- Detección de proyectos vacíos

#### 🔍 Detección inteligente
- `detectors.py`: Identifica 11+ lenguajes (Python, JS, TS, Go, Rust, Java, etc.)
- Detecta frameworks: Flask, Django, FastAPI, Express, Vue, React, Angular
- Detecta monorepos: Lerna, pnpm, Nx, Turborepo
- Detecta servicios systemd en sistemas Linux

#### 🛠️ Extracción de metadatos
- `extractors.py`: Extrae funciones/clases con regex avanzados
- Soporta Python (`def`, `class`), JavaScript/TS (`function`, `class`, arrow functions)
- Detecta endpoints REST: Flask/FastAPI (`@app.route`), Express (`app.get/post`)
- Extrae componentes Vue con props, emits y llamadas API
- Mapea dependencias (imports/requires) entre archivos

#### 📝 Generación de documentación
- `all_generators.py`: Genera 5 archivos YAML automatizados
  * `PROJECT_INDEX.yaml` - Índice completo de archivos y funciones con líneas exactas
  * `CONVENTIONS.yaml` - Patrones de código detectados
  * `TESTING.yaml` - Comandos de validación (syntax check, tests)
  * `ERRORS.yaml` - Template para registrar errores
  * `GIT_WORKFLOW.yaml` - Flujo de trabajo git sugerido
- `CLAUDE.md` - Instrucciones para agentes de IA
- `.cursorrules` - Symlink automático para Cursor IDE
- `README.md` - Documentación del proyecto con badges y guías

#### 🧪 Sistema de tests
- `tests/test_all.py`: 7 tests unitarios
  * TestValidators: Python version, Git installed
  * TestScanner: Empty projects, file scanning
  * TestDetectors: Language detection
  * TestExtractors: Function extraction
  * TestTemplates: Template suggestion
- Ejecución: `python3 tests/test_all.py`
- Resultados: **7/7 tests passing** ✅

#### 🔄 Actualización incremental
- `.ai/update_index.py`: Reescanea proyecto sin reinstalar todo
- Regenera solo `PROJECT_INDEX.yaml` preservando otros archivos
- Detecta nuevos archivos, funciones y dependencias
- Uso: `python3 .ai/update_index.py`

#### ✅ Validación de entorno
- `validators.py`: Verifica Python 3.7+, Git, permisos de escritura, espacio en disco
- Modo de advertencias con `--verbose` flag
- Mensajes de error descriptivos en español

#### 🎨 Templates de proyectos
- 12 tipos soportados: Python (script/Flask/Django/FastAPI), Node/Express, React, Vue, Go, Rust, Java, Generic
- Sugerencia automática basada en stack detectado
- Estructura de carpetas y convenciones específicas por framework

#### 🧠 Auto-documentación (Dogfooding)
- **Wizard se aplica a sí mismo** su propio sistema `.ai/`
- Genera índice con 19 archivos, 54 funciones
- Prueba de concepto exitosa: Sistema funcional

### 🐛 Bugs corregidos
- ✅ ImportError con imports relativos → Cambiado a absolute imports
- ✅ `extract_components` inexistente → Renombrado a `extract_vue_components`
- ✅ `detect_frameworks()` recibía argumento extra → Corregida firma
- ✅ `generate_project_index()` orden de parámetros → Ajustado en update_index.py
- ✅ Tests no detectados → Agregado `tests/__init__.py`

### 📦 Infraestructura
- Sin dependencias externas (solo Python 3.7+ stdlib)
- `.gitignore` configurado (Python, venv, IDE, OS files)
- `LICENSE` MIT incluida
- `requirements.txt` vacío (explícitamente sin deps)

### 📚 Documentación
- README.md completo con:
  * Características principales
  * Instrucciones de instalación
  * Arquitectura del proyecto
  * Ejemplos de uso del índice
  * Comandos útiles
  * Templates soportados
  * Detección automática de frameworks
- CLAUDE.md con instrucciones para agentes
- Comentarios docstring en todas las funciones

### 📊 Estadísticas
- **28 archivos** creados
- **2183 líneas** de código
- **54 funciones/clases** implementadas
- **7 tests** unitarios (100% passing)
- **19 archivos** indexados en el wizard
- **0 dependencias** externas

### 🎯 Validación
- ✅ Instalación en modo auto: `python3 install.py --auto`
- ✅ Tests: `python3 tests/test_all.py` (7/7 OK)
- ✅ Actualización: `python3 .ai/update_index.py`
- ✅ Git: Commit inicial + tag v1.0.0
- ✅ Auto-aplicación: Wizard genera su propio `.ai/`

---

## Próximas versiones (Roadmap)

### [1.1.0] - Mejoras planificadas
- [ ] Embeber PROMPT_CREATE_AI_INDEX.md en generadores
- [ ] Detectar más lenguajes (Kotlin, Swift, Scala)
- [ ] Soporte para GraphQL endpoint detection
- [ ] Extracción de tests (pytest, jest, mocha)
- [ ] Modo diff: Comparar índice viejo vs nuevo
- [ ] CI/CD templates (GitHub Actions, GitLab CI)

### [1.2.0] - Integraciones
- [ ] Plugin VSCode para visualizar índice
- [ ] GitHub Action para auto-actualizar índice en PRs
- [ ] Soporte para workspaces multi-proyecto
- [ ] API REST para consultar índice remotamente

---

## Comandos ejecutados (validación final)

```bash
# Tests unitarios
python3 tests/test_all.py
# Resultado: Ran 7 tests in 0.003s - OK

# Auto-instalación
python3 install.py --auto
# Resultado: 19 archivos, 54 funciones indexadas

# Actualización de índice
python3 .ai/update_index.py
# Resultado: ✓ Actualizado: 19 archivos, 54 funciones, 0 endpoints

# Git commit
git init && git add -A && git commit -m "feat(wizard): initial release AI Agent Wizard v1.0.0"
git tag -a v1.0.0 -m "Initial release"
# Resultado: 28 files changed, 2183 insertions(+)
```

---

**Creado por:** AI Agent Wizard  
**Fecha:** 2026-01-11  
**Versión:** 1.0.0  
**Líneas de código:** 2183  
**Files:** 28
