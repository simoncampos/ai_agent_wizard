#!/usr/bin/env python3
"""
Script para actualizar PROJECT_INDEX.yaml sin reinstalar todo el sistema .ai/
Uso: python .ai/update_index.py
"""

import os
import sys
from pathlib import Path

# Agregar src al path
project_dir = Path(__file__).parent.parent
sys.path.insert(0, str(project_dir / 'src'))

from core.scanner import scan_files
from core.detectors import detect_languages, detect_frameworks
from core.extractors import extract_functions, extract_endpoints, extract_vue_components, extract_dependencies
from generators.all_generators import generate_project_index


def update_index():
    """Actualiza PROJECT_INDEX.yaml analizando cambios en el código"""
    
    print("Actualizando PROJECT_INDEX.yaml...")
    
    # Escanear archivos
    print("  [1/4] Escaneando archivos...")
    files_map = scan_files(project_dir, show_progress=True)
    
    # Detectar stack
    print("  [2/4] Detectando stack tecnológico...")
    languages = detect_languages(project_dir, files_map.keys())
    frameworks = detect_frameworks(project_dir)
    
    # Extraer información
    print("  [3/4] Extrayendo código...")
    functions = extract_functions(files_map)
    endpoints = extract_endpoints(files_map)
    components = extract_vue_components(files_map)
    dependencies = extract_dependencies(files_map)
    
    # Generar índice
    print("  [4/4] Generando PROJECT_INDEX.yaml...")
    yaml_content = generate_project_index(
        str(project_dir),
        project_dir.name,
        languages,
        frameworks,
        files_map,
        functions,
        endpoints,
        components,
        dependencies
    )
    
    # Guardar
    index_path = project_dir / '.ai' / 'PROJECT_INDEX.yaml'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    
    total_functions = sum(len(funcs) for funcs in functions.values())
    total_endpoints = sum(len(eps) for eps in endpoints.values())
    
    print(f"\n✓ Actualizado: {len(files_map)} archivos, {total_functions} funciones, {total_endpoints} endpoints")


if __name__ == '__main__':
    try:
        update_index()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
