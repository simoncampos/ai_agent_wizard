# AI Agent Wizard 🧙‍♂️

**Sistema automatizado de indexación y documentación para proyectos de software**

Optimiza la interacción con agentes de IA reduciendo el consumo de tokens hasta en un 95%, permitiendo que Claude, GPT y otros asistentes encuentren código relevante sin leer archivos completos.

---

## 🎯 Características

- ✅ **Sin dependencias externas** - Solo Python 3.7+ stdlib
- 📊 **Indexación automática** - Escanea y mapea todo el código fuente
- 🔍 **Detección inteligente** - Identifica lenguajes, frameworks y arquitectura
- 📝 **Documentación autogenerada** - Crea guías de convenciones y testing
- 🐛 **Registro de errores** - Mantiene historial de problemas y soluciones
- 🔄 **Actualización incremental** - Reescanea cambios sin reinstalar
- 🧠 **Auto-documentado** - El wizard se aplica a sí mismo su propio sistema

---

## 🚀 Instalación

### Instalación rápida (modo automático)

```bash
python3 install.py --auto
```

### Con progreso detallado (modo verbose)

```bash
python3 install.py --auto --verbose
```

### Instalación interactiva

```bash
python3 install.py
```

### Ver todas las opciones

```bash
python3 install.py --help
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
| `CLAUDE.md` | 🤖 Instrucciones para agentes de IA (Claude, Copilot, etc.) |
| `.cursorrules` | ⚙️ Symlink a CLAUDE.md para Cursor IDE |
| `update_index.py` | 🔄 Script para actualizar el índice después de cambios |

---

## 🏗️ Arquitectura

```
AI_AGENT_WIZARD/
├── src/
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
├── tests/
│   └── test_all.py              # Tests unitarios (7 tests)
├── install.py                   # Wrapper de instalación
└── .ai/                         # Sistema autogenerado
    ├── PROJECT_INDEX.yaml       # Archivos y funciones indexadas
    └── update_index.py          # Script de actualización

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

**Beneficio**: El agente puede buscar `install` en `main.py:45` directamente sin leer las 215 líneas.

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

**Versión:** 1.0.0  
**Generado por:** AI Agent Wizard
