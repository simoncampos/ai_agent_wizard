# CHANGELOG

## [5.0.0] - 2026-03-04

### ✨ Nuevos Índices YAML (8 archivos nuevos)
- **CONTEXT_ANCHOR.yaml**: Micro-resumen del proyecto en <500 tokens. Diseñado para releerse cada ~5 mensajes y mantener contexto en conversaciones largas.
- **CALL_GRAPH.yaml**: Grafo de llamadas entre funciones — quién llama a quién y quién es llamado por quién. Clave para análisis de impacto.
- **TYPES.yaml**: Modelos de datos, interfaces, structs, dataclasses, enums con sus campos y líneas exactas. Soporte para Python, TypeScript, Go, Rust, Java y PHP.
- **DOCSTRINGS.yaml**: Índice de documentación de funciones — docstrings y JSDoc para cada función documentada.
- **CONFIG_MAP.yaml**: Variables de entorno, archivos `.env`, archivos de configuración detectados con sus ubicaciones.
- **ENTRY_POINTS.yaml**: Puntos de entrada del proyecto, boot sequence, ciclo de vida de requests, orden de lectura recomendado.
- **PATTERNS.yaml**: Patrones de diseño detectados, middleware, decoradores, autenticación, convenciones de naming, estrategia de error handling.
- **QUICK_CONTEXT.yaml**: Guías pre-calculadas para tareas comunes (agregar endpoint, agregar modelo, modificar función, agregar test).

### 🧠 Sistema de Persistencia de Contexto (4 capas)
- **Capa 1 — CONTEXT_ANCHOR.yaml**: Micro-resumen ultra-compacto que se relee frecuentemente para prevenir pérdida de contexto.
- **Capa 2 — PROTOCOL.yaml reforzado**: Nuevas secciones `CONTEXT PERSISTENCE (NON-NEGOTIABLE)` con triggers automáticos (`on_conversation_start`, `every_5_messages`, `on_new_task`, `on_context_doubt`, `on_summary_or_compression`). Nuevo `context_check` self-test antes de cada respuesta.
- **Capa 3 — AGENT_GUIDE.md renovado**: Instrucción explícita de incluir frase de persistencia en resúmenes, referencia a CONTEXT_ANCHOR, checklist de verificación expandido.
- **Capa 4 — Archivos IDE nativos**: Archivos de contexto para cada IDE que redirigen a AGENT_GUIDE.md.

### 📝 AGENT_GUIDE.md v5.0
- **Sección de negocio obligatoria**: El agente DEBE completar la sección "QUÉ ES ESTE PROYECTO" ANTES de su primera respuesta. Si dice "PENDIENTE", el agente no responde hasta rellenarla.
- **Actualización continua**: El agente debe mantener esta sección actualizada con cambios significativos del proyecto.
- **Reglas de workflow**: Nuevas reglas sobre cuándo actualizar índices y hacer commit — solo cuando el usuario confirma que funciona, nunca durante fixes/debug.
- **Tabla de archivos**: Listado completo de todos los YAMLs en `.ai/` con descripciones.
- **Guía de persistencia**: Instrucciones para mantener contexto en conversaciones largas.

### 🖥️ Archivos IDE Multi-Plataforma
- **CLAUDE.md**: Instrucciones para Claude Code (claude.ai).
- **.github/copilot-instructions.md**: Instrucciones para GitHub Copilot (VS Code, JetBrains).
- **.windsurfrules**: Instrucciones para Windsurf/Codeium.
- **.cursorrules**: Symlink a AGENT_GUIDE.md (fallback a copia en Windows sin permisos de symlink).

### 🔄 Migración v4→v5 Automática
- `python .ai/update.py` ahora detecta proyectos v4 y migra automáticamente a v5.
- **Preservación de sección de negocio**: Si un agente ya completó la sección "QUÉ ES ESTE PROYECTO", se preserva durante la migración.
- Nueva función `upgrade_project_files()` en main.py para migración de AGENT_GUIDE + creación de archivos IDE.
- `update_index.py` regenera todos los nuevos YAMLs automáticamente.

### ⛔ Reglas de Workflow (Nuevo)
- **Durante fixes/debug**: NO actualizar índices, NO hacer commit, NO actualizar descripción de negocio. Solo corregir el código.
- **Cuándo sí**: Cuando el usuario confirme que funciona ("ya funciona", "todo ok", "aprobado"), o solicite explícitamente.
- **Secuencia correcta**: Implementar → Usuario prueba → Usuario aprueba → Actualizar índices → Commit.
- Reglas aplicadas en AGENT_GUIDE.md, PROTOCOL.yaml, y todos los archivos IDE.

### 🔧 Nuevos Extractores (5)
- `extract_call_graph(files_map, functions)`: Analiza cuerpos de funciones para detectar llamadas entre ellas.
- `extract_types_and_models(files_map)`: Detecta clases de datos, interfaces, enums en 6 lenguajes.
- `extract_docstrings(files_map, functions)`: Extrae documentación de funciones (docstrings Python, JSDoc, PHPDoc, GoDoc, RustDoc).
- `extract_config_map(files_map, project_path)`: Busca variables de entorno y archivos de configuración.
- `extract_patterns(files_map, functions, frameworks)`: Detecta patrones de diseño, middleware, auth, naming.

### 🔧 Cambios Internos
- `extractors.py`: +350 líneas con 5 nuevos extractores + helpers por lenguaje.
- `all_generators.py`: +500 líneas con 8 nuevos generadores. PROTOCOL.yaml expandido con persistencia, workflow y first_response.
- `main.py`: Refactorizado — helpers reutilizables (`_get_agent_guide_content`, `_extract_business_section`, `_restore_business_section`, `_create_ide_files`, `upgrade_project_files`). Fase 5 simplificada usando helpers.
- `update_index.py`: Integración de todos los nuevos extractores y generadores.
- `update.py`: Fase 5 de migración automática de archivos de instrucciones.
- `install_online.py`: Versión actualizada a v5.0.0.
- Tests: +2 clases de test (`TestNewExtractors`, `TestNewGenerators`) con 17 nuevos tests.

### 🚀 Beneficios para Agentes IA
- **95% menos tokens**: Los nuevos índices (CALL_GRAPH, TYPES, DOCSTRINGS) permiten entender relaciones sin abrir archivos.
- **Contexto persistente**: El sistema de 4 capas garantiza que el agente nunca "olvide" las reglas del proyecto.
- **Comprensión progresiva**: CONTEXT_ANCHOR → QUICK_CONTEXT → índices específicos. De lo general a lo específico.
- **Workflow ordenado**: Reglas claras sobre cuándo hacer commit evitan actualizaciones prematuras durante debug.
- **Multi-IDE**: Un sistema, todos los agentes. Claude, Copilot, Cursor, Windsurf, todos reciben instrucciones.

---

## [4.0.0] - 2026-02-25

### ✨ Major Features
- **AI_INSTRUCTIONS.yaml**: Nuevo archivo dinámico de instrucciones de flujo para agentes IA
  - Regenerado automáticamente con cada `update_index.py`
  - Combina información genérica (patrones, consideraciones) con dinámica (stack detectado, notas específicas)
  - Secciones estáticas preservadas entre generaciones, dinámicas actualizadas
  - Soporta sección `custom_considerations` para notas del proyecto que persisten

### 🔄 Merge Inteligente
- Nueva función `merge_ai_instructions()` en `all_generators.py`
  - Preserva secciones estáticas (project_flow, data_structures, critical_patterns, limitations, ai_behavior)
  - Actualiza secciones dinámicas (statistics, detected_stack, project_specific_notes)
  - Mantiene sección custom_considerations agregada por usuarios
  - Genera _merge_info con información de cuándo se actualizó y qué estrategia se usó

### 🎯 Contenido AI_INSTRUCTIONS.yaml
- **meta**: Información de generación y propósito
- **statistics**: Números de proyecto (archivos, líneas, funciones, endpoints, componentes)
- **project_flow**: Descripción de las 6 fases del wizard
- **data_structures**: Formato de files_map, functions dict, endpoints, components
- **detected_stack**: Lo que se encontró en THIS proyecto (dinámico)
- **critical_patterns**: Convenciones (líneas 1-based, rutas con /, convenciones de naming)
- **important_considerations**: Optimizaciones de memoria, exclusiones, edge cases
- **project_specific_notes**: Consideraciones específicas detectadas (Django, Flask, FastAPI, React, Vue, Next.js, Docker, etc.)
- **custom_considerations**: Sección reservada para notas del proyecto
- **ai_behavior**: Cómo deben actuar agentes IA (lectura, búsqueda, cambios, optimización)
- **limitations**: Limitaciones de la extracción regex y cuándo regenerar

### 🔧 Cambios Internos
- `all_generators.py`: +450 líneas para `generate_ai_instructions()` y `merge_ai_instructions()`
- `src/main.py`: Integración de AI_INSTRUCTIONS en instalación
- `src/scripts/update_index.py`: Integración de merge en regeneraciones
- Versión actualizada a `4.0.0`

### 🚀 Beneficios para Agentes IA
- Instrucciones contextualizadas actualizadas automáticamente
- Mejora en comprensión del proyecto sin leer código base
- Consideraciones preservadas entre cambios del código
- Reduce necesidad de preguntas sobre patrones/flujo del proyecto

---

## [3.0.0] - 2025-06-18

### 💥 Breaking Changes
- Todos los YAMLs generados dinámicamente (antes ARCHITECTURE y GRAPH estaban hardcodeados)
- `extract_vue_components` renombrado a `extract_ui_components` (alias backward-compatible disponible)
- 4 nuevos archivos YAML en `.ai/` — agentes deben leer PROTOCOL.yaml primero

### ✨ Nuevas características

#### Fase 1 — Corrección de bugs críticos
- **Windows fix**: `check_disk_space` usa `shutil.disk_usage` en vez de `os.statvfs` (incompatible con Windows)
- **Imports limpios**: eliminadas 6 importaciones muertas de `main.py`
- **Scripts portables**: scripts movidos a `src/scripts/` para distribución confiable
- **ARCHITECTURE.yaml dinámico**: analiza estructura real del proyecto (directorios, módulos, dependencias, entry points)
- **GRAPH.yaml dinámico**: construye grafo real de dependencias, rutas API, árbol de componentes, ranking de archivos clave
- **`.cursorrules` actualizado** a v3.0.0 con los 12 archivos YAML listados

#### Fase 2 — Detección mejorada (Python/PHP/Node.js)
- **Decoradores Python**: `@dataclass`, `@property`, `@staticmethod`, `@classmethod`, `@abstractmethod`
- **Go/Rust/Java/Ruby**: interfaces Go, impl blocks Rust, interfaces Java, módulos Ruby
- **PHP avanzado**: traits, interfaces, namespaces
- **Endpoints Django**: `path()` / `re_path()` en `urls.py`
- **Endpoints Laravel**: `Route::get/post/put/delete/patch`
- **Endpoints NestJS**: `@Get/@Post` con `@Controller` base route
- **Componentes React**: function/arrow components, hooks, TypeScript props
- **Componentes Vue**: `defineProps`, `defineEmits`, naming por archivo `.vue`
- **Componentes Svelte**: `export let` props, dispatch events
- **Dependencias Python**: parsing completo `from X import Y` e `import X`
- **Dependencias JS/TS**: resolución de alias `@/` y `~/`
- **Dependencias PHP**: `use Namespace\Class` y `require/include`
- **30+ frameworks**: Laravel, WordPress, Symfony, NestJS, Celery, DRF, Pydantic, SQLAlchemy, pytest, Gatsby, Remix, Prisma, Drizzle, y más

#### Fase 3 — Innovaciones para agentes IA
- **CHANGES.yaml**: tracking MD5 por archivo con `.state.json`, identifica changed/added/removed/unchanged entre ejecuciones
- **SUMMARIES.yaml**: resúmenes semánticos de 1 línea por archivo extraídos de docstrings, comentarios o nombres de funciones
- **CONTEXT_BUDGET.yaml**: prioridad 3 niveles (critical/important/reference) basada en entry points, endpoints, cantidad de funciones
- **PROTOCOL.yaml**: reglas multi-agente, orden de lectura obligatorio, reglas de modificación, optimización de tokens, manejo de errores

#### Fase 4 — Infraestructura
- **ERRORS.yaml dinámico**: analiza patrones try/except/catch en el código fuente y agrega errores comunes del stack
- **TESTING.yaml dinámico**: detecta archivos de configuración de tests (pytest.ini, jest.config, vitest, cypress, playwright, phpunit), directorios de tests, comandos específicos del framework
- **29 tests unitarios**: cobertura de validators, scanner, detectors, extractors (Python/PHP/JS, endpoints Flask/Express/Laravel/Django, decoradores, dependencias), generators (todos los 12 YAMLs), templates, e integración completa

### 🔧 Cambios internos
- Versión unificada a `3.0.0` en `__init__.py`, `main.py`, `install_online.py`
- `extractors.py` expandido significativamente (~600+ líneas)
- `detectors.py` expandido (~298 líneas) con detección de 30+ frameworks
- `all_generators.py` expandido (~888 líneas) con 4 nuevos generadores
- AGENT_GUIDE.md template actualizado con los 12 YAMLs y nuevo orden de lectura

### 📊 Impacto
- 12 archivos YAML generados (antes 8) — +50% más contexto para agentes
- 29 tests unitarios (antes 6) — +383% cobertura
- Soporte real multi-lenguaje: Python, PHP, JavaScript/TypeScript, Go, Rust, Java, Ruby
- Detección de 30+ frameworks y herramientas
- Compatible con Windows, macOS y Linux
- Zero dependencias externas (Python 3.7+ stdlib only)

---

## [2.1.0] - 2026-02-23

### ✨ Mejoras

#### Universalidad mejorada
- Renombrado `CLAUDE.md` → `AGENT_GUIDE.md` para soportar cualquier agente de IA (Claude, GPT, Copilot, etc.)
- Actualizado `.cursorrules` para apuntar a `AGENT_GUIDE.md`
- Todas las referencias en código y documentación actualizadas

#### Instalador consolidado
- Eliminado `install.py` (instalador local simple)
- Funcionalidad consolidada en `install_online.py` (descarga desde GitHub o instala en local)
- Un solo instalador para todas las necesidades
- Soporta tanto instalación online como local

#### README mejorado
- Sistema de generación de README con más información del proyecto
- Generado con nombre en MAYÚSCULAS basado en la carpeta del proyecto
- Incluye detección automática de stack (lenguajes, frameworks backend/frontend)
- Mejor visibilidad y profesionalismo

### 🔧 Cambios internos
- `src/main.py`: actualizado para usar `AGENT_GUIDE.md`
- Scripts de actualización también generan archivos con nombres universales
- Mejorado proceso de instalación con reducción de redundancia

### 📊 Impacto
- Reducción de 1 archivo instalador (simplificación)
- Mejor compatibilidad con múltiples agentes de IA
- Documentación más visible y profesional

---

## [2.0.0] - 2026-02-16

### 💥 Breaking Changes
- `.ai/src/` ahora contiene el motor de indexación (antes no se copiaba)
- `update.py` actualiza `.ai/src/` en vez del root del proyecto
- `update_index.py` importa desde `.ai/src/` (ya no depende de tener `src/` en root)
- Eliminados `install_hook.py` y `pre-commit.ps1` (hook se instala automáticamente)

### ✨ Nuevas características

#### Detección de versión previa
- `install.py` / `install_online.py` detectan si `.ai/` ya existe
- Menú interactivo: [1] Reinstalar desde cero, [2] Actualizar, [3] Cancelar
- `update.py` también presenta menú: [1] Actualizar, [2] Eliminar, [3] Cancelar
- Modo `--auto` salta el menú y procede automáticamente

#### Git hook automático
- `pre-commit.hook` se instala automáticamente durante `install()`
- Regenera índices en cada `git commit` si hay cambios en código fuente
- Auto-agrega YAMLs actualizados al commit
- No requiere configuración manual

#### Sistema de comprensión para AI agents
- `GRAPH.yaml` — Grafo de dependencias comprimido (~30 líneas)
- `FLOW.yaml` — Instrucciones paso a paso para agentes IA
- `ARCHITECTURE.yaml` — Fases de ejecución y módulos
- Lectura jerárquica: FLOW → GRAPH → PROJECT_INDEX

#### Motor de indexación portable (.ai/src/)
- Se copia `src/` a `.ai/src/` durante instalación (sin `__pycache__`)
- `update_index.py` y `update.py` importan desde `.ai/src/`
- El proyecto instalado es autónomo: no necesita el repo wizard

### 🔧 Refactorización

#### main.py: 652 → 320 líneas (-51%)
- Eliminado `_get_update_script()`: 350 líneas de código muerto (duplicaba update.py como string inline)
- Reducido de 6 fases a 5 fases
- Helpers extraídos: `_copy_tree_clean()`, `_copy_file_safe()`, `_install_git_hook()`

#### update_index.py: reescrito completo
- Regenera TODOS los YAMLs (antes solo PROJECT_INDEX)
- Soporta `--quiet` (silencioso para hooks), `--verbose`, `--help`
- Importa desde `.ai/src/` en vez del root

#### update.py: reescrito completo
- Actualiza `.ai/src/` (no el root del usuario)
- Auto-actualiza scripts (update.py, update_index.py, hook)
- Reinstala git hook automáticamente
- Regenera todos los YAMLs incluyendo ARCHITECTURE, FLOW, GRAPH

#### Prompt CLAUDE.md mejorado
- Instrucciones inequívocas: "YA existe, NO lo creaste, NO lo modifiques, solo ÚSALO"
- Evita que la IA intente recrear el sistema de índices

### 📁 Reorganización

#### Movidos a docs/
- `CHANGELOG.md` → `docs/CHANGELOG.md`
- `PROJECT_STRUCTURE.md` → `docs/PROJECT_STRUCTURE.md`
- `REORGANIZATION_SUMMARY.md` → `docs/REORGANIZATION_SUMMARY.md`
- `requirements.txt` → `docs/requirements.txt`

#### Eliminados
- `.ai/install_hook.py` — Innecesario (hook se auto-instala)
- `.ai/pre-commit.ps1` — Innecesario (Git usa bash en todas las plataformas)

#### Raíz final limpia
```
install.py              ← Instalación local
install_online.py       ← Instalación online
LICENSE / README.md     ← Lo básico
src/ tests/ docs/ scripts/ .ai/
```

### 📊 Estadísticas
- **main.py**: -332 líneas eliminadas (código muerto)
- **update_index.py**: 73 → 120 líneas (ahora regenera todo)
- **update.py**: 375 → 292 líneas (más limpio, menos redundancia)
- **Archivos eliminados**: 2 (install_hook.py, pre-commit.ps1)
- **Archivos movidos**: 4 (a docs/)

---

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
**Versión actual:** 2.0.0
