# 🚀 Instalación Rápida - AI Agent Wizard

## ¿Qué es esto?

Sistema que crea un índice inteligente de tu proyecto para que agentes de IA (Claude, GPT, Copilot) encuentren código sin navegar archivos completos.

**Resultado**: 95% menos tokens, acceso directo a funciones con número de línea exacto.

---

## 📥 Instalar (Un solo comando)

### Linux / macOS

```bash
curl -O https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py && python3 install_online.py --auto
```

### Windows (PowerShell)

```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py" -OutFile "install_online.py"; python install_online.py --auto
```

### Windows (con curl)

```bash
curl -O https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py && python install_online.py --auto
```

---

## ✨ ¿Qué hace?

1. Descarga el sistema automáticamente
2. Escanea tu proyecto
3. Crea carpeta `.ai/` con índices:
   - `PROJECT_INDEX.yaml` - Todas las funciones con líneas exactas
   - `CONVENTIONS.yaml` - Patrones de código
   - `TESTING.yaml` - Comandos de validación
   - `ERRORS.yaml` - Errores conocidos
4. Borra archivos temporales (limpieza automática)

**Solo queda** el sistema `.ai/` en tu proyecto.

---

## 💡 Ejemplo de uso

**Antes (sin AI Agent Wizard)**:
```
"Encuentra la función que valida emails"
→ Agente busca en 20 archivos
→ Lee 5,000 líneas de código
→ Usa 8,000 tokens
→ Tarda 2-3 minutos
```

**Después (con AI Agent Wizard)**:
```
"Encuentra la función que valida emails"
→ Agente abre .ai/PROJECT_INDEX.yaml
→ Encuentra: src/auth/validators.py:validate_email (línea 234)
→ Lee solo líneas 234-245
→ Usa 150 tokens
→ Tarda 10 segundos
```

---

## 🔧 Requisitos

- Python 3.7 o superior
- Conexión a internet (solo durante instalación)
- Git (opcional, pero recomendado)

---

## 📖 Uso del sistema

### Para agentes de IA

Dile a tu agente:
```
"Lee .ai/PROJECT_INDEX.yaml antes de buscar cualquier función.
Usa los números de línea del índice para leer solo código relevante."
```

### Actualizar después de cambios

```bash
python3 .ai/update_index.py
```

---

## 🌐 Alternativas de instalación

### Método 1: Dos pasos (descargar + ejecutar)

```bash
# 1. Descargar instalador
curl -O https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py

# 2. Ejecutar (puedes usarlo en múltiples proyectos)
python3 install_online.py --auto
```

### Método 2: Clonar repositorio completo

```bash
git clone https://github.com/simoncampos/ai_agent_wizard.git
cd ai_agent_wizard
python3 install.py --auto
```

### Método 3: Instalación con progreso detallado (verbose)

```bash
curl -O https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py
python3 install_online.py --auto --verbose
```

---

## 🎯 Instalación en proyecto específico

```bash
# Instalar en proyecto actual
cd /path/to/mi-proyecto
python3 install_online.py --auto

# O especificar ruta
python3 install_online.py /path/to/otro-proyecto --auto
```

---

## ❓ Problemas Comunes

### "No hay conexión a internet"

Usa el instalador local:
```bash
git clone https://github.com/simoncampos/ai_agent_wizard.git
cd ai_agent_wizard
python3 install.py --auto
```

### "python3: command not found"

Intenta con `python` en vez de `python3`:
```bash
python install_online.py --auto
```

### "ModuleNotFoundError"

El instalador online no tiene dependencias externas. Si ves este error, es del código del proyecto donde estás instalando, no del wizard.

---

## 📊 Soporte de Lenguajes

- **Backend**: Python, JavaScript, TypeScript, Go, Rust, Java, PHP, Ruby, C, C++
- **Frontend**: React, Vue, Angular, Svelte
- **Frameworks**: Flask, Django, FastAPI, Express, Next.js, Nuxt

---

## 🔒 Seguridad

- ✅ Solo descarga desde GitHub oficial (HTTPS)
- ✅ Sin dependencias externas (solo Python stdlib)
- ✅ Código fuente abierto y auditable
- ✅ Limpieza automática de archivos temporales

---

## 📚 Más Información

- 📖 [Documentación completa](https://github.com/simoncampos/ai_agent_wizard)
- 🛠️ [Guía técnica del instalador](https://github.com/simoncampos/ai_agent_wizard/blob/main/INSTALL_ONLINE.md)
- 🚀 [Guía rápida de uso](https://github.com/simoncampos/ai_agent_wizard/blob/main/QUICKSTART_ONLINE.md)

---

## 🙏 Créditos

Desarrollado para optimizar la interacción con Claude Sonnet, GPT-4 y otros agentes de IA.

**Licencia**: MIT  
**Versión**: 1.1.0
