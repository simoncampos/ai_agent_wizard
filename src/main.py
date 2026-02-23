#!/usr/bin/env python3
"""
AI Agent Wizard - Main Entry Point
Indexación inteligente para agentes de IA: reduce tokens 95%, elimina navegación.
"""

import os
import sys
import shutil
from pathlib import Path

# Agregar directorio src al path para imports
src_dir = os.path.dirname(os.path.abspath(__file__))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from core.scanner import scan_files, iter_source_files
from core.detectors import detect_languages, detect_frameworks
from core.extractors import extract_functions, extract_endpoints, extract_vue_components, extract_dependencies
from core.validators import validate_environment
from generators.all_generators import (
    generate_project_index, generate_all_yamls,
    generate_architecture_yaml, generate_flow_yaml, generate_graph_yaml,
    generate_changes_yaml, generate_summaries_yaml,
    generate_context_budget_yaml, generate_protocol_yaml
)
from utils.warnings import set_verbose, warn, show_warnings_summary, vprint

VERSION = "3.0.0"


# ============================================================================
# HELPERS
# ============================================================================

def _copy_tree_clean(src, dst):
    """Copia directorio excluyendo __pycache__ y .pyc"""
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))


def _copy_file_safe(src_path, dst_path):
    """Copia un archivo si existe. Retorna True si copió."""
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
        return True
    return False


def _install_git_hook(project_path, ai_dir):
    """Instala pre-commit hook si .git/ existe"""
    git_hooks_dir = os.path.join(project_path, '.git', 'hooks')
    hook_src = os.path.join(ai_dir, 'pre-commit.hook')

    if not os.path.isdir(git_hooks_dir) or not os.path.exists(hook_src):
        return False

    try:
        hook_dst = os.path.join(git_hooks_dir, 'pre-commit')
        shutil.copy2(hook_src, hook_dst)
        if os.name != 'nt':
            os.chmod(hook_dst, 0o755)
        return True
    except Exception:
        return False


# ============================================================================
# INSTALL
# ============================================================================

def install(project_path, auto_mode=False, verbose=False):
    """
    Instala el sistema .ai/ en un proyecto.
    
    Crea índices YAML, copia el motor de indexación a .ai/src/,
    instala scripts de actualización y configura git hook automático.
    """
    set_verbose(verbose)

    project_path = os.path.abspath(project_path)
    project_name = os.path.basename(project_path)

    print(f"\n  Proyecto: {project_name}")
    print(f"  Ruta: {project_path}")

    # ── Detectar instalación previa ───────────────────────────────────
    ai_dir_check = os.path.join(project_path, '.ai')
    if os.path.isdir(ai_dir_check) and not auto_mode:
        print(f"\n  ⚠  Se detectó una instalación previa de .ai/")
        print(f"")
        print(f"  Opciones:")
        print(f"    [1] Eliminar actual e instalar desde cero")
        print(f"    [2] Actualizar (mantener datos, actualizar motor + índices)")
        print(f"    [3] Cancelar")
        choice = input(f"\n  Elige [1/2/3]: ").strip()

        if choice == '3' or (choice and choice not in ['1', '2']):
            print("\n  Cancelado.\n")
            return False
        elif choice == '2':
            # Delegar a update.py
            update_script = os.path.join(ai_dir_check, 'update.py')
            if os.path.exists(update_script):
                print("\n  Delegando a update.py...\n")
                import subprocess
                result = subprocess.run(
                    [sys.executable, update_script, '--auto'],
                    cwd=project_path
                )
                return result.returncode == 0
            else:
                print("  No se encontró .ai/update.py. Se reinstalará desde cero.")
        # choice == '1': eliminar y continuar
        print("\n  🗑️  Eliminando instalación anterior...", end="", flush=True)
        shutil.rmtree(ai_dir_check)
        print(" ✓")
    elif os.path.isdir(ai_dir_check) and auto_mode:
        # En modo auto, reinstalar desde cero sin preguntar
        shutil.rmtree(ai_dir_check)

    # ── [1/5] Validación ──────────────────────────────────────────────
    if not auto_mode:
        print("\n  [1/5] Validando entorno...")
        all_ok, checks = validate_environment(project_path)
        for check_name, (status, msg) in checks.items():
            icon = "✓" if status else "✗"
            print(f"       {icon} {check_name}: {msg}")
        if not all_ok:
            print("\n  ERROR: Faltan requisitos.")
            return False

    # ── [2/5] Detección ───────────────────────────────────────────────
    print(f"\n  [2/5] Detectando stack tecnológico...")

    files_map = scan_files(project_path, show_progress=not verbose)
    vprint(f"Archivos escaneados: {len(files_map)}", level=1)

    languages = detect_languages(project_path, iter_source_files(project_path))
    print(f"         Lenguajes: {', '.join(languages) if languages else 'ninguno'}")

    frameworks = detect_frameworks(project_path)
    print(f"         Backend: {', '.join(frameworks['backend']) if frameworks['backend'] else '-'}")
    print(f"         Frontend: {', '.join(frameworks['frontend']) if frameworks['frontend'] else '-'}")

    # ── [3/5] Extracción ──────────────────────────────────────────────
    print(f"\n  [3/5] Extrayendo información del código...")

    functions = extract_functions(files_map)
    total_funcs = sum(len(v) for v in functions.values())
    print(f"         {total_funcs} funciones/clases")

    endpoints = extract_endpoints(files_map)
    print(f"         {len(endpoints)} endpoints API")

    components = extract_vue_components(files_map)
    print(f"         {len(components)} componentes UI")

    dependencies = extract_dependencies(files_map)
    print(f"         {len(dependencies)} archivos con dependencias")

    # Liberar contenido de memoria
    for fpath in files_map:
        if 'content' in files_map[fpath]:
            del files_map[fpath]['content']

    # ── [4/5] Crear sistema .ai/ ──────────────────────────────────────
    print(f"\n  [4/5] Creando sistema .ai/...")
    ai_dir = os.path.join(project_path, '.ai')
    os.makedirs(ai_dir, exist_ok=True)

    # — Índices YAML —
    index_content = generate_project_index(
        project_path, project_name, languages, frameworks,
        files_map, functions, endpoints, components, dependencies
    )
    with open(os.path.join(ai_dir, 'PROJECT_INDEX.yaml'), 'w', encoding='utf-8') as f:
        f.write(index_content)
    print("         PROJECT_INDEX.yaml")

    yamls = generate_all_yamls(project_name, languages, frameworks, project_path, files_map)
    for filename, content in yamls.items():
        with open(os.path.join(ai_dir, filename), 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"         {filename}")

    arch_content = generate_architecture_yaml(
        project_path, languages, frameworks, files_map, functions, dependencies
    )
    with open(os.path.join(ai_dir, 'ARCHITECTURE.yaml'), 'w', encoding='utf-8') as f:
        f.write(arch_content)
    print("         ARCHITECTURE.yaml")

    flow_content = generate_flow_yaml()
    with open(os.path.join(ai_dir, 'FLOW.yaml'), 'w', encoding='utf-8') as f:
        f.write(flow_content)
    print("         FLOW.yaml")

    graph_content = generate_graph_yaml(dependencies, functions, endpoints, components)
    with open(os.path.join(ai_dir, 'GRAPH.yaml'), 'w', encoding='utf-8') as f:
        f.write(graph_content)
    print("         GRAPH.yaml")

    changes_content = generate_changes_yaml(project_path, files_map)
    with open(os.path.join(ai_dir, 'CHANGES.yaml'), 'w', encoding='utf-8') as f:
        f.write(changes_content)
    print("         CHANGES.yaml")

    summaries_content = generate_summaries_yaml(files_map, functions)
    with open(os.path.join(ai_dir, 'SUMMARIES.yaml'), 'w', encoding='utf-8') as f:
        f.write(summaries_content)
    print("         SUMMARIES.yaml")

    budget_content = generate_context_budget_yaml(files_map, functions, endpoints, components)
    with open(os.path.join(ai_dir, 'CONTEXT_BUDGET.yaml'), 'w', encoding='utf-8') as f:
        f.write(budget_content)
    print("         CONTEXT_BUDGET.yaml")

    protocol_content = generate_protocol_yaml()
    with open(os.path.join(ai_dir, 'PROTOCOL.yaml'), 'w', encoding='utf-8') as f:
        f.write(protocol_content)
    print("         PROTOCOL.yaml")

    # — Motor de indexación (.ai/src/) —
    _copy_tree_clean(src_dir, os.path.join(ai_dir, 'src'))
    vprint("Motor copiado a .ai/src/", level=1)

    # — Scripts de actualización —
    scripts_dir = os.path.join(src_dir, 'scripts')
    for script in ['update.py', 'update_index.py', 'pre-commit.hook']:
        if _copy_file_safe(os.path.join(scripts_dir, script), os.path.join(ai_dir, script)):
            print(f"         {script}")

    # — Git hook automático —
    if _install_git_hook(project_path, ai_dir):
        print("         pre-commit hook ✓")

    # ── [5/5] Archivos de instrucciones ───────────────────────────────
    print(f"\n  [5/5] Creando archivos de instrucciones...")

    agent_guide_content = f"""# {project_name} - Instrucciones para Agentes de IA

## IMPORTANTE: Lee esto antes de hacer cualquier cosa
Este proyecto YA tiene un sistema de índice instalado en `.ai/`.
NO lo creaste tú. NO lo modifiques. NO intentes recrearlo.
Solo ÚSALO para trabajar de forma eficiente.

## Tu primer paso OBLIGATORIO
Antes de leer o modificar cualquier archivo del proyecto, lee estos archivos (ya existen):
1. `.ai/PROTOCOL.yaml` — Reglas de comportamiento para agentes IA
2. `.ai/FLOW.yaml` — Te explica cómo usar el sistema de índices
3. `.ai/PROJECT_INDEX.yaml` — Mapa completo: cada función, endpoint y componente con su archivo y línea exacta
4. `.ai/CONTEXT_BUDGET.yaml` — Qué archivos leer primero según prioridad

## Reglas de trabajo
- NUNCA leas un archivo completo si solo necesitas una función. Busca su ubicación en PROJECT_INDEX.yaml primero.
- SIEMPRE usa los números de línea del índice para leer solo la sección relevante.
- NUNCA modifiques nada dentro de `.ai/`. Es generado automáticamente.
- Consulta `.ai/CHANGES.yaml` para ver qué archivos cambiaron recientemente.
- Consulta `.ai/SUMMARIES.yaml` para un resumen rápido de cada archivo.
- Si el usuario modifica código y necesita actualizar índices: `python .ai/update_index.py`

## Qué hay en .ai/ (NO TOCAR)
- `PROJECT_INDEX.yaml` — Funciones, endpoints, componentes con líneas exactas
- `GRAPH.yaml` — Dependencias entre módulos (lectura rápida)
- `ARCHITECTURE.yaml` — Estructura del proyecto y módulos
- `FLOW.yaml` — Instrucciones de uso para ti
- `CHANGES.yaml` — Archivos modificados desde la última indexación
- `SUMMARIES.yaml` — Resúmenes semánticos de cada archivo
- `CONTEXT_BUDGET.yaml` — Prioridad de lectura por archivo
- `PROTOCOL.yaml` — Reglas de comportamiento para agentes IA
- `CONVENTIONS.yaml` — Convenciones de código del proyecto
- `TESTING.yaml` — Cómo ejecutar tests
- `ERRORS.yaml` — Errores conocidos
- `GIT_WORKFLOW.yaml` — Política de commits y ramas
- `update_index.py` — Regenera índices (el usuario lo ejecuta, no tú)
- `update.py` — Actualiza el motor (el usuario lo ejecuta, no tú)
- `src/` — Motor interno de indexación (NUNCA modificar)
"""

    agent_guide_path = os.path.join(project_path, 'AGENT_GUIDE.md')
    with open(agent_guide_path, 'w', encoding='utf-8') as f:
        f.write(agent_guide_content)
    print("         AGENT_GUIDE.md")

    try:
        cursorrules = os.path.join(project_path, '.cursorrules')
        if not os.path.exists(cursorrules):
            os.symlink('AGENT_GUIDE.md', cursorrules)
            print("         .cursorrules -> AGENT_GUIDE.md")
    except Exception:
        pass

    readme_path = os.path.join(project_path, 'README.md')
    if not os.path.exists(readme_path):
        readme_content = f"""# {project_name}

Sistema de optimización de contexto para agentes de IA instalado.

## Stack
- **Lenguajes**: {', '.join(languages)}
- **Backend**: {', '.join(frameworks['backend']) if frameworks['backend'] else 'N/A'}
- **Frontend**: {', '.join(frameworks['frontend']) if frameworks['frontend'] else 'N/A'}

## .ai/
Consulta `.ai/FLOW.yaml` para entender el sistema de índices.

Generado por **AI Agent Wizard v{VERSION}**
"""
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("         README.md")

    # ── Resumen ───────────────────────────────────────────────────────
    show_warnings_summary()

    print(f"\n  {'=' * 60}")
    print(f"  ✅ INSTALACIÓN COMPLETADA")
    print(f"  {'=' * 60}")
    print(f"  Archivos indexados:  {len(files_map)}")
    print(f"  Funciones extraídas: {total_funcs}")
    print(f"  Endpoints API:       {len(endpoints)}")
    print(f"  Componentes UI:      {len(components)}")
    print(f"\n  📖 Siguiente paso:")
    print(f"     Lee .ai/FLOW.yaml para usar el sistema de índices")
    print(f"  {'=' * 60}\n")

    return True


# ============================================================================
# ENTRY POINT
# ============================================================================

def main():
    """Entry point principal"""
    print("\n  " + "=" * 60)
    print(f"  AI AGENT WIZARD v{VERSION}")
    print("  Indexación inteligente: menos tokens, cero navegación")
    print("  " + "=" * 60)

    auto_mode = '--auto' in sys.argv
    verbose = '--verbose' in sys.argv or '-v' in sys.argv

    if '--help' in sys.argv or '-h' in sys.argv:
        print("""
  USO:
    python install.py [ruta_proyecto] [opciones]
  
  OPCIONES:
    --auto          Modo no interactivo
    --verbose, -v   Modo debug detallado
    --help, -h      Muestra esta ayuda
  
  EJEMPLOS:
    python install.py                   # Proyecto actual
    python install.py /path/proyecto    # Ruta específica
    python install.py --auto --verbose  # Auto + debug
        """)
        sys.exit(0)

    args = [a for a in sys.argv[1:] if not a.startswith('--') and not a.startswith('-')]
    project_path = args[0] if args else os.getcwd()

    success = install(project_path, auto_mode=auto_mode, verbose=verbose)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
