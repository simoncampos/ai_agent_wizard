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

from core.scanner import scan_files, is_empty_project, iter_source_files
from core.detectors import detect_languages, detect_frameworks, detect_services, detect_monorepo
from core.extractors import extract_functions, extract_endpoints, extract_vue_components, extract_dependencies
from core.validators import validate_environment
from templates.project_templates import suggest_template, create_structure, list_templates
from generators.all_generators import (
    generate_project_index, generate_all_yamls,
    generate_architecture_yaml, generate_flow_yaml, generate_graph_yaml
)
from utils.warnings import set_verbose, warn, show_warnings_summary, vprint


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
    wizard_root = os.path.dirname(src_dir)  # Raíz del wizard (padre de src/)

    print(f"\n  Proyecto: {project_name}")
    print(f"  Ruta: {project_path}")

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

    yamls = generate_all_yamls(project_name, languages, frameworks)
    for filename, content in yamls.items():
        with open(os.path.join(ai_dir, filename), 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"         {filename}")

    arch_content = generate_architecture_yaml(project_path)
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

    # — Motor de indexación (.ai/src/) —
    _copy_tree_clean(src_dir, os.path.join(ai_dir, 'src'))
    vprint("Motor copiado a .ai/src/", level=1)

    # — Scripts de actualización —
    wizard_ai = os.path.join(wizard_root, '.ai')
    for script in ['update.py', 'update_index.py', 'pre-commit.hook']:
        if _copy_file_safe(os.path.join(wizard_ai, script), os.path.join(ai_dir, script)):
            print(f"         {script}")

    # — Git hook automático —
    if _install_git_hook(project_path, ai_dir):
        print("         pre-commit hook ✓")

    # ── [5/5] Archivos de instrucciones ───────────────────────────────
    print(f"\n  [5/5] Creando archivos de instrucciones...")

    claude_content = f"""# Instrucciones para Agentes de IA - {project_name}

## Sistema de Índice (.ai/)
Este proyecto tiene un sistema de índice optimizado en `.ai/` que te permite:
- Acceder directamente a funciones con números de línea exactos
- Evitar leer archivos completos innecesariamente
- Reducir consumo de tokens hasta 95%

ANTES de leer o modificar cualquier archivo fuente, lee:
1. `.ai/FLOW.yaml` - Cómo usar el sistema (empieza aquí)
2. `.ai/GRAPH.yaml` - Grafo de dependencias comprimido
3. `.ai/PROJECT_INDEX.yaml` - Mapa completo (funciones + líneas exactas)

## Reglas
- NUNCA leas un archivo completo si solo necesitas una función específica
- SIEMPRE consulta el índice primero para ubicar código (archivo + línea)
- USA los números de línea del índice para leer solo secciones relevantes

## Actualización
- Índices: `python .ai/update_index.py`
- Core:    `python .ai/update.py`

Generado por AI Agent Wizard v1.0.0
"""

    claude_path = os.path.join(project_path, 'CLAUDE.md')
    with open(claude_path, 'w', encoding='utf-8') as f:
        f.write(claude_content)
    print("         CLAUDE.md")

    try:
        cursorrules = os.path.join(project_path, '.cursorrules')
        if not os.path.exists(cursorrules):
            os.symlink('CLAUDE.md', cursorrules)
            print("         .cursorrules -> CLAUDE.md")
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

Generado por **AI Agent Wizard v1.0.0**
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
    print("  AI AGENT WIZARD v1.0.0")
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
