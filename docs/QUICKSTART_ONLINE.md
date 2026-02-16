# Guía Rápida: Instalador Online

## 📦 Para usuarios finales (una vez configurado el repo)

### Un solo comando
```bash
curl -O https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py && python3 install_online.py --auto
```

### Dos pasos (descargar y ejecutar)
```bash
# 1. Descargar instalador (una sola vez)
curl -O https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py

# 2. Ejecutar (puede usarse en múltiples proyectos)
python3 install_online.py --auto
```

### Con wget (alternativa a curl)
```bash
wget https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py
python3 install_online.py --auto
```

---

## ⚙️ Para mantenedores (configurar una vez)

### Paso 1: Configurar repositorio

**Opción A: Edición manual**
```bash
# Editar install_online.py línea 28
GITHUB_REPO = "tu-usuario/ai-agent-wizard"  # Cambiar
```

**Opción B: Script automático (recomendado)**
```bash
python3 configure_online_installer.py tu-usuario/ai-agent-wizard
```

### Paso 2: Subir a GitHub
```bash
git add install_online.py
git commit -m "feat: configurar instalador online"
git push origin main
```

### Paso 3: Compartir con usuarios
```bash
# URL pública del instalador
https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py
```

---

## 🎯 Casos de uso

### Instalar en proyecto actual
```bash
cd mi-proyecto
curl -O https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py
python3 install_online.py --auto
```

### Instalar en proyecto específico
```bash
python3 install_online.py /ruta/al/proyecto --auto
```

### Instalar con debug (ver progreso)
```bash
python3 install_online.py --auto --verbose
```

### Instalar interactivamente (con confirmación)
```bash
python3 install_online.py
# Te pedirá confirmar antes de descargar
```

---

## 📊 Qué hace el instalador

```
1. Verifica internet ✓
2. Descarga repo desde GitHub (< 500 KB)
3. Extrae archivos temporalmente
4. Instala sistema .ai/ en tu proyecto
5. Genera: PROJECT_INDEX.yaml, CONVENTIONS.yaml, etc.
6. BORRA todos los archivos descargados
7. Solo queda el sistema .ai/ en tu proyecto
```

**Resultado**: Tu proyecto ahora tiene `.ai/` con índices optimizados.

---

## 🗑️ Limpieza automática

El instalador elimina automáticamente:
- ✅ ZIP descargado (~100 KB)
- ✅ Código extraído (~300 KB)
- ✅ Directorio temporal completo

**Solo permanece**: El sistema `.ai/` en tu proyecto.

---

## ⚡ Comparación de métodos

| Método | Tamaño descarga | Requiere Git | Limpieza | Actualización |
|--------|----------------|--------------|----------|---------------|
| **Online** | 12 KB inicial + 500 KB temp (auto-borrado) | ❌ No | ✅ Auto | Siempre última |
| **git clone** | 300 KB permanente | ✅ Sí | Manual | `git pull` |
| **Local** | 0 (ya descargado) | ❌ No | N/A | Manual |

---

## 🔒 Seguridad

- ✅ Descarga solo desde GitHub oficial (HTTPS)
- ✅ Valida estructura antes de ejecutar
- ✅ No ejecuta scripts de terceros
- ✅ Limpieza garantizada (try/finally)
- ✅ Usa directorios temporales del OS

---

## 🐛 Si algo falla

### Error: "No hay conexión a internet"
```bash
# Verificar
ping github.com

# Alternativa: instalador local
git clone https://github.com/simoncampos/ai_agent_wizard.git
cd ai_agent_wizard
python3 install.py --auto
```

### Error: "La configuración del repositorio no está completa"
✅ Este error ya no debería aparecer - el repositorio está configurado como `simoncampos/ai_agent_wizard`.

Si lo ves, significa que descargaste una versión antigua del instalador.
- Solución: Descarga la última versión desde GitHub

### Instalación interrumpida (Ctrl+C)
- No te preocupes: los archivos temporales se borran automáticamente
- Puedes reintentar inmediatamente

---

## 💡 Tips

### Reutilizar instalador
```bash
# Descargar una vez
curl -O https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py

# Usar en múltiples proyectos
python3 install_online.py ~/proyecto1 --auto
python3 install_online.py ~/proyecto2 --auto
python3 install_online.py ~/proyecto3 --auto
```

### Agregar a scripts de setup
```bash
# setup.sh
#!/bin/bash
curl -O https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py
python3 install_online.py --auto
rm install_online.py
```

### Integrar con CI/CD
```yaml
# .github/workflows/setup.yml
- name: Setup AI Agent Wizard
  run: |
    curl -O https://raw.githubusercontent.com/simoncampos/ai_agent_wizard/main/install_online.py
    python3 install_online.py --auto
```

---

## 📞 Soporte

- **Documentación técnica**: Ver [INSTALL_ONLINE.md](INSTALL_ONLINE.md)
- **Código fuente**: Ver [install_online.py](install_online.py)
- **Issues**: GitHub issues del repositorio
