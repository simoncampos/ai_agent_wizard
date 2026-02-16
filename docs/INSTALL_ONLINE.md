# Instalador Online - Documentación Técnica

## 📋 Descripción

`install_online.py` es un instalador autónomo que descarga la última versión de AI Agent Wizard desde GitHub, la instala en el proyecto actual y limpia automáticamente todos los archivos temporales.

## 🎯 Flujo de Instalación

```
┌─────────────────────────────────────────────────────────┐
│  1. Usuario ejecuta install_online.py                   │
└───────────────┬─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│  2. Verificación de internet y configuración            │
│     ✓ Conexión a GitHub                                 │
│     ✓ URL del repositorio configurada                   │
└───────────────┬─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│  3. Descarga del repositorio                             │
│     • Crea directorio temporal                           │
│     • Descarga ZIP desde GitHub                          │
│     • Muestra progreso (opcional)                        │
└───────────────┬─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│  4. Extracción de archivos                               │
│     • Descomprime ZIP en temporal                        │
│     • Localiza carpeta src/                              │
│     • Valida estructura del código                       │
└───────────────┬─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│  5. Instalación del sistema                              │
│     • Importa src/main.py desde temporal                 │
│     • Ejecuta install() en proyecto actual               │
│     • Genera carpeta .ai/ con índices                    │
└───────────────┬─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│  6. Limpieza automática                                  │
│     • Elimina directorio temporal completo               │
│     • Borra ZIP descargado                               │
│     • Remueve código extraído                            │
└───────────────┬─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│  7. Sistema .ai/ listo en el proyecto                    │
│     ✓ INDEX_PROJECT.yaml                                │
│     ✓ CONVENTIONS.yaml                                   │
│     ✓ TESTING.yaml, ERRORS.yaml, etc.                   │
└─────────────────────────────────────────────────────────┘
```

## 🔧 Configuración

### Variables principales (líneas 28-29)

```python
GITHUB_REPO = "simoncampos/ai_agent_wizard"
GITHUB_BRANCH = "main"       # Rama a descargar
```

**✅ Configurado para**: `simoncampos/ai_agent_wizard`

## 📝 Modos de Uso

### Modo Automático
```bash
python3 install_online.py --auto
```
- Sin interacción del usuario
- Ideal para CI/CD y scripts automatizados
- Usa configuración por defecto

### Modo Verbose
```bash
python3 install_online.py --auto --verbose
```
- Muestra progreso detallado de descarga
- Útil para debugging
- Muestra rutas de archivos temporales

### Modo Interactivo
```bash
python3 install_online.py
```
- Pide confirmación antes de instalar
- Muestra resumen de lo que se instalará
- Permite cancelar antes de descargar

### Proyecto Específico
```bash
python3 install_online.py /path/to/project --auto
```
- Instala en proyecto específico
- Útil para múltiples proyectos

## 🔒 Seguridad

### Verificaciones implementadas

1. **Conexión HTTPS**: Solo descarga vía HTTPS de github.com
2. **Validación de estructura**: Verifica que exista carpeta `src/` antes de instalar
3. **Limpieza garantizada**: Usa `try/finally` para limpiar incluso si hay errores
4. **Directorio temporal**: Usa `tempfile.mkdtemp()` en ubicación segura del OS

### Código ejecutado

El instalador solo ejecuta código del repositorio oficial configurado en `GITHUB_REPO`. No ejecuta scripts de terceros ni permite redirecciones.

## 🗑️ Archivos Temporales

### Ubicación
- **Linux/Mac**: `/tmp/ai_agent_wizard_XXXXXX/`
- **Windows**: `C:\Users\USER\AppData\Local\Temp\ai_agent_wizard_XXXXXX\`

### Contenido temporal (eliminado automáticamente)
```
ai_agent_wizard_XXXXXX/
├── ai_agent_wizard.zip          # ZIP descargado (~100KB)
└── ai-agent-wizard-main/        # Código extraído
    ├── src/
    │   ├── main.py
    │   ├── core/
    │   ├── generators/
    │   └── templates/
    ├── tests/
    └── README.md
```

**⏱️ Duración**: Los archivos solo existen durante la instalación (~10-30 segundos).

### Limpieza manual (en caso de error)

Si la instalación se interrumpe:
```bash
# Linux/Mac
rm -rf /tmp/ai_agent_wizard_*

# Windows PowerShell
Remove-Item "$env:TEMP\ai_agent_wizard_*" -Recurse -Force
```

## 📊 Tamaño de Descarga

- **ZIP del repositorio**: ~50-150 KB (comprimido)
- **Código extraído**: ~200-300 KB
- **Ancho de banda total**: < 500 KB por instalación

## ⚡ Ventajas vs Instalación Local

| Característica | Online | Local (git clone) |
|----------------|--------|-------------------|
| Tamaño inicial | 1 archivo (12 KB) | Todo el repo (~300 KB) |
| Siempre actualizado | ✅ Sí | ❌ Requiere `git pull` |
| Funciona sin git | ✅ Sí | ❌ Requiere git |
| Limpieza automática | ✅ Sí | ➖ Manual opcional |
| Velocidad | ~10-15s | ~5s |
| Requiere internet | ✅ Sí | Solo primera vez |

## 🐛 Troubleshooting

### Error: "No hay conexión a internet"
```bash
# Verificar conectividad
ping github.com

# Alternativa: usar instalador local
git clone https://github.com/simoncampos/ai_agent_wizard.git
cd ai_agent_wizard
python3 install.py --auto
```

### Error: "No se encontró carpeta 'src'"
- El repositorio puede estar mal configurado
- Verificar que `GITHUB_REPO` y `GITHUB_BRANCH` sean correctos
- Probar manualmente: `https://github.com/simoncampos/ai_agent_wizard/tree/main`

### Error: "No se pudo descargar el repositorio"
Posibles causas:
- Repositorio privado (requiere autenticación)
- URL incorrecta en `GITHUB_REPO`
- Rate limit de GitHub (esperar 1 minuto)
- Firewall bloqueando github.com

### Instalación interrumpida
Si presionas Ctrl+C durante la instalación:
- Los archivos temporales se limpian automáticamente
- No queda basura en el sistema
- Puedes reintentar inmediatamente

## 🔄 Actualización del Sistema

Para actualizar un proyecto que ya tiene el sistema instalado:

```bash
# Descargar instalador online
curl -O https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py

# Reinstalar (sobrescribe .ai/ con versión actualizada)
python3 install_online.py --auto

# Limpiar instalador online
rm install_online.py
```

El instalador detecta si ya existe `.ai/` y actualiza los archivos sin perder datos personalizados en `ERRORS.yaml` o `CONVENTIONS.yaml`.

## 📦 Distribución

### Método recomendado para usuarios finales

**Opción 1: Un solo comando (requiere curl/wget)**
```bash
curl -O https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py && python3 install_online.py --auto
```

**Opción 2: Descarga + ejecución separadas**
```bash
# Descargar
curl -O https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py

# Ejecutar cuando quieras
python3 install_online.py --auto
```

### Agregar a package managers

**NPM (package.json)**
```json
{
  "scripts": {
    "setup-ai": "curl -O https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py && python3 install_online.py --auto"
  }
}
```

**Makefile**
```makefile
setup-ai:
	@curl -O https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py
	@python3 install_online.py --auto
	@rm install_online.py
```

## 🧪 Testing

Probar el instalador online en proyecto de prueba:

```bash
# Crear proyecto de prueba
mkdir /tmp/test_project
cd /tmp/test_project

# Crear archivo ejemplo
echo "print('Hello')" > main.py

# Ejecutar instalador
python3 /path/to/install_online.py --auto --verbose

# Verificar instalación
ls -la .ai/
cat .ai/PROJECT_INDEX.yaml

# Limpiar
cd ..
rm -rf /tmp/test_project
```

## 📝 Notas de Implementación

- **Sin dependencias**: Solo usa `urllib`, `zipfile`, `tempfile` de stdlib
- **Python 3.7+**: Compatible con versiones modernas
- **Cross-platform**: Funciona en Linux, macOS, Windows
- **Idempotente**: Puede ejecutarse múltiples veces sin efectos adversos
- **Atómico**: Si falla, no deja basura en el proyecto
