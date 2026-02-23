# 🔄 Guía de Actualización - AI Agent Wizard

Hay tres formas de mantener tu sistema actualizado:

---

## 1️⃣ Actualizar Core (Motor + Scripts + Índices)

**Cuando quieras descargar la última versión del sistema `.ai/` desde GitHub:**

Este comando:
1. ✅ Descarga la última versión del core desde GitHub
2. ✅ Actualiza `.ai/src/` (motor de indexación)
3. ✅ Actualiza scripts (`update.py`, `update_index.py`, `pre-commit.hook`)
4. ✅ **Regenera automáticamente todos los índices**

```bash
python .ai/update.py
```

### Opciones:

```bash
# Modo no interactivo (sin preguntas)
python .ai/update.py --auto

# Con progreso detallado
python .ai/update.py --verbose

# Ver opciones
python .ai/update.py --help
```

**Duración**: ~30-60 segundos (depende de la conexión a internet)

---

## 2️⃣ Regenerar Índices Después de Cambios

**Cuando solo cambió tu código y quieres actualizar los índices YAML:**

```bash
python .ai/update_index.py
```

### Opciones:

```bash
# Modo silencioso (solo errores)
python .ai/update_index.py --quiet

# Con progreso detallado
python .ai/update_index.py --verbose

# Ver opciones
python .ai/update_index.py --help
```

### Qué regenera:
- `PROJECT_INDEX.yaml` - Mapa de funciones, endpoints, componentes
- `ARCHITECTURE.yaml` - Estructura y fases de ejecución
- `GRAPH.yaml` - Grafo de dependencias comprimido
- `FLOW.yaml` - Instrucciones para agentes de IA
- `CONVENTIONS.yaml`, `TESTING.yaml`, `ERRORS.yaml`, `GIT_WORKFLOW.yaml`

**Duración**: ~5-10 segundos (dependiendo del tamaño del proyecto)

---

## 3️⃣ Automático con Git Hook (Recomendado)

Si tienes repositorio Git inicializado (`.git/`), el hook se instala automáticamente durante la instalación:

```
.git/hooks/pre-commit
```

### Qué hace automáticamente:
- ✅ Antes de cada commit en Git, regenera los índices si hay cambios en código
- ✅ Los YAMLs actualizados se incluyen automáticamente en el commit
- ✅ **Nunca tendrás índices desincronizados de tu código**

### Cómo funciona:

```bash
# Haces cambios en tu código
git add .
git commit -m "feat: nueva funcionalidad"  
# ← El hook se ejecuta automáticamente aquí
# ← Regenera índices automáticamente
# ← Los YAML actualizados se incluyen en el commit
```

**Ventaja**: Sin intervención manual, siempre sincronizado

---

## 🔄 Flujo recomendado

### Desarrollo normal:
```bash
# Haces cambios en tu código
# El git hook se ejecuta automáticamente en cada commit
git add .
git commit -m "feat: nueva funcionalidad"  # ← Hook regenera índices
```

### Cuando subes nueva versión del Wizard:
```bash
# Descarga e instala core actualizado
# Regenera automáticamente todos los índices
python .ai/update.py --auto
```

### Después de cambios mayores (si el hook falla):
```bash
# Solo regenerar índices con detalle
python .ai/update_index.py --verbose
```

---

## 📊 Comparación de métodos

| Acción | Comando | Duración | Cuándo |
|--------|---------|----------|--------|
| **Actualizar todo** | `python .ai/update.py --auto` | ~30-60s | Cuando hay nueva versión del core (mensual) |
| **Regenerar índices** | `python .ai/update_index.py` | ~5-10s | Después de cambios mayores no capturados por hook |
| **Automático (hook)** | (Se ejecuta solo) | <1s | En cada git commit |

---

## ❓ Solución de problemas

### El comando `update.py` no funciona

Asegúrate de estar en el directorio del proyecto:

```bash
# Correcto
cd /ruta/a/tu/proyecto
python .ai/update.py

# Incorrecto
python /ruta/a/tu/proyecto/.ai/update.py
```

### El hook no se ejecuta automáticamente

Verifica que Git está inicializado:

```bash
ls .git/hooks/pre-commit
```

Si no existe, tu proyecto no es un repositorio Git. Inicializa con:

```bash
git init
```

Luego reinstala el hook:

```bash
python .ai/update.py --auto
```

### Los índices se ven desactualizados

Ejecuta manualmente:

```bash
python .ai/update_index.py --verbose
```

### Error al descargar el core

Verifica que tienes conexión a internet:

```bash
# Prueba conexión
ping github.com
```

Si hay problemas de certificado SSL, el script intenta sin verificación (inseguro pero funcional).

---

## 📝 Archivos involucrados en actualizaciones

**Core** (actualizado por `update.py`):
- `.ai/src/` - Motor de indexación
- `.ai/update.py` - Este actualizador
- `.ai/update_index.py` - Regenerador de índices
- `.ai/pre-commit.hook` - Git hook automático

**Índices** (regenerados por `update_index.py`):
- `PROJECT_INDEX.yaml` - Mapa completo del proyecto
- `ARCHITECTURE.yaml` - Arquitectura y flujo
- `CONVENTIONS.yaml` - Patrones detectados
- `TESTING.yaml` - Comandos de testing
- `ERRORS.yaml` - Errores conocidos
- `GIT_WORKFLOW.yaml` - Política de commits
- `FLOW.yaml` - Guía para agentes IA
- `GRAPH.yaml` - Grafo de dependencias

---

## 🚀 Próximos pasos después de actualizar

```bash
# Ver cambios en el índice
head -30 .ai/PROJECT_INDEX.yaml

# Revisar flujo actualizado
cat .ai/FLOW.yaml

# Ver arquitectura detectada
cat .ai/ARCHITECTURE.yaml
```

---

## 💡 Consejos

1. **Para desarrollo activo**: El git hook se encarga automáticamente
2. **Antes de hacer push**: Ejecuta `python .ai/update_index.py --verbose` una última vez
3. **Cuando subes cambios mayores**: También actualiza el core con `python .ai/update.py`
4. **En CI/CD**: Usa `python .ai/update.py --auto` para actualizar automáticamente en pipelines
