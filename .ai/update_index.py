#!/usr/bin/env python3
"""
AI Agent Wizard - Regenerar índices localmente
Regenera todos los archivos YAML en .ai/ después de cambios en el código.

USO:
    python .ai/update_index.py [opciones]

OPCIONES:
    --quiet         Solo errores (para hooks)
    --verbose, -v   Progreso detallado
    --help, -h      Mostrar esta ayuda
"""

import os
import sys
from pathlib import Path

# Paths
ai_dir = Path(__file__).parent
project_dir = ai_dir.parent
engine_dir = ai_dir / 'src'

# Verificar que el motor existe
if not engine_dir.is_dir():
    print("ERROR: No se encontró .ai/src/ (motor de indexación)")
    print("Ejecuta: python .ai/update.py  para restaurarlo")
    sys.exit(1)

# Importar desde .ai/src/
sys.path.insert(0, str(engine_dir))

from core.scanner import scan_files, iter_source_files
from core.detectors import detect_languages, detect_frameworks
from core.extractors import extract_functions, extract_endpoints, extract_vue_components, extract_dependencies
from generators.all_generators import (
    generate_project_index, generate_all_yamls,
    generate_architecture_yaml, generate_flow_yaml, generate_graph_yaml
)


def update_all(quiet=False, verbose=False):
    """Regenera todos los índices YAML en .ai/"""
    project_name = project_dir.name

    if not quiet:
        print("  Regenerando índices...\n")

    # 1. Escanear
    if not quiet:
        print("  [1/4] Escaneando archivos...")
    files_map = scan_files(str(project_dir), show_progress=False)
    if verbose:
        print(f"         {len(files_map)} archivos encontrados")

    # 2. Detectar
    if not quiet:
        print("  [2/4] Detectando stack...")
    languages = detect_languages(str(project_dir), iter_source_files(str(project_dir)))
    frameworks = detect_frameworks(str(project_dir))

    # 3. Extraer
    if not quiet:
        print("  [3/4] Extrayendo código...")
    functions = extract_functions(files_map)
    endpoints = extract_endpoints(files_map)
    components = extract_vue_components(files_map)
    dependencies = extract_dependencies(files_map)

    # Liberar contenido
    for fpath in files_map:
        if 'content' in files_map[fpath]:
            del files_map[fpath]['content']

    # 4. Generar todos los YAML
    if not quiet:
        print("  [4/4] Generando YAMLs...")

    generated = []

    # PROJECT_INDEX.yaml
    content = generate_project_index(
        str(project_dir), project_name, languages, frameworks,
        files_map, functions, endpoints, components, dependencies
    )
    _write(ai_dir / 'PROJECT_INDEX.yaml', content)
    generated.append('PROJECT_INDEX.yaml')

    # CONVENTIONS, TESTING, ERRORS, GIT_WORKFLOW
    yamls = generate_all_yamls(project_name, languages, frameworks)
    for filename, content in yamls.items():
        _write(ai_dir / filename, content)
        generated.append(filename)

    # ARCHITECTURE.yaml
    content = generate_architecture_yaml(str(project_dir))
    _write(ai_dir / 'ARCHITECTURE.yaml', content)
    generated.append('ARCHITECTURE.yaml')

    # FLOW.yaml
    content = generate_flow_yaml()
    _write(ai_dir / 'FLOW.yaml', content)
    generated.append('FLOW.yaml')

    # GRAPH.yaml
    content = generate_graph_yaml(dependencies, functions, endpoints, components)
    _write(ai_dir / 'GRAPH.yaml', content)
    generated.append('GRAPH.yaml')

    # Resumen
    total_funcs = sum(len(v) for v in functions.values())

    if not quiet:
        print(f"\n  ✓ {len(generated)} archivos regenerados")
        print(f"    {len(files_map)} archivos | {total_funcs} funciones | {len(endpoints)} endpoints")
        if verbose:
            for f in generated:
                print(f"    → {f}")


def _write(path, content):
    """Escribe contenido a archivo"""
    with open(str(path), 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    if '--help' in sys.argv or '-h' in sys.argv:
        print(__doc__)
        sys.exit(0)

    quiet = '--quiet' in sys.argv
    verbose = '--verbose' in sys.argv or '-v' in sys.argv

    try:
        update_all(quiet=quiet, verbose=verbose)
    except Exception as e:
        if not quiet:
            print(f"  ERROR: {e}")
        sys.exit(1)
