#!/usr/bin/env python3
"""
AI Agent Wizard - Main Entry Point
Sistema de optimización de contexto para agentes de IA
"""

import os
import sys
from pathlib import Path

# Agregar directorio src al path para imports
src_dir = os.path.dirname(os.path.abspath(__file__))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Imports ahora funcionan como módulos locales
from core.scanner import scan_files, is_empty_project, iter_source_files
from core.detectors import detect_languages, detect_frameworks, detect_services, detect_monorepo
from core.extractors import extract_functions, extract_endpoints, extract_vue_components, extract_dependencies
from core.validators import validate_environment
from templates.project_templates import suggest_template, create_structure, list_templates
from generators.all_generators import generate_project_index, generate_all_yamls
from utils.warnings import set_verbose, warn, show_warnings_summary, vprint


def install(project_path, auto_mode=False, verbose=False):
    """
    Proceso principal de instalación del sistema .ai/
    
    Args:
        project_path: Ruta absoluta del proyecto
        auto_mode: Si True, no pide confirmaciones interactivas  
        verbose: Si True, muestra debug detallado
    """
    set_verbose(verbose)
    
    project_path = os.path.abspath(project_path)
    project_name = os.path.basename(project_path)
    
    print(f"\n  Proyecto: {project_name}")
    print(f"  Ruta: {project_path}")
    
    # Validaciones de entorno
    if not auto_mode:
        print("\n  [1/6] Validando entorno...")
        all_ok, checks = validate_environment(project_path)
        for check_name, (status, msg) in checks.items():
            icon = "✓" if status else "✗"
            print(f"       {icon} {check_name}: {msg}")
        
        if not all_ok:
            print("\n  ERROR: Faltan requisitos.")
            return False
    
    # Fase 2: Detección
    print(f"\n  [2/6] Detectando stack tecnológico...")
    
    # Escanear archivos
    files_map = scan_files(project_path, show_progress=not verbose)
    vprint(f"Archivos escaneados: {len(files_map)}", level=1)
    
    # Detectar lenguajes
    from core.scanner import iter_source_files
    languages = detect_languages(project_path, iter_source_files(project_path))
    print(f"         Lenguajes: {', '.join(languages) if languages else 'ninguno'}")
    
    # Detectar frameworks
    frameworks = detect_frameworks(project_path)
    print(f"         Backend: {', '.join(frameworks['backend']) if frameworks['backend'] else '-'}")
    print(f"         Frontend: {', '.join(frameworks['frontend']) if frameworks['frontend'] else '-'}")
    
    # Fase 3: Extracción
    print(f"\n  [3/6] Extrayendo información del código...")
    functions = extract_functions(files_map)
    total_funcs = sum(len(v) for v in functions.values())
    print(f"         {total_funcs} funciones/clases")
    
    endpoints = extract_endpoints(files_map)
    print(f"         {len(endpoints)} endpoints API")
    
    components = extract_vue_components(files_map)
    print(f"         {len(components)} componentes UI")
    
    dependencies = extract_dependencies(files_map)
    print(f"         {len(dependencies)} archivos con dependencias")
    
    # Limpiar content
    for fpath in files_map:
        del files_map[fpath]['content']
    
    # Fase 4: Crear .ai/
    print(f"\n  [4/6] Creando sistema .ai/...")
    ai_dir = os.path.join(project_path, '.ai')
    os.makedirs(ai_dir, exist_ok=True)
    
    # PROJECT_INDEX.yaml
    index_content = generate_project_index(
        project_path, project_name, languages, frameworks,
        files_map, functions, endpoints, components, dependencies
    )
    with open(os.path.join(ai_dir, 'PROJECT_INDEX.yaml'), 'w', encoding='utf-8') as f:
        f.write(index_content)
    print("         PROJECT_INDEX.yaml")
    
    # Otros YAMLs
    yamls = generate_all_yamls(project_name, languages, frameworks)
    for filename, content in yamls.items():
        with open(os.path.join(ai_dir, filename), 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"         {filename}")
    
    # Fase 5: CLAUDE.md
    print(f"\n  [5/6] Creando archivos de instrucciones...")
    claude_content = f"""# Instrucciones para Agentes de IA - {project_name}

## Sistema de Indice (.ai/)
Este proyecto tiene un sistema de índice optimizado en `.ai/`.
ANTES de leer o modificar cualquier archivo fuente, lee:

1. `.ai/PROJECT_INDEX.yaml` - Mapa completo del proyecto
2. `.ai/CONVENTIONS.yaml` - Patrones de código
3. `.ai/TESTING.yaml` - Comandos de validación
4. `.ai/ERRORS.yaml` - Errores conocidos
5. `.ai/GIT_WORKFLOW.yaml` - Políticas de git

## Reglas
- NUNCA leas un archivo completo si solo necesitas una función
- SIEMPRE usa el índice para obtener números de línea exactos
- SIEMPRE ejecuta validaciones después de modificar código

Generado por AI Agent Wizard v1.0.0
"""
    
    claude_path = os.path.join(project_path, 'CLAUDE.md')
    with open(claude_path, 'w', encoding='utf-8') as f:
        f.write(claude_content)
    print("         CLAUDE.md")
    
    # Crear symlinks básicos
    try:
        cursorrules = os.path.join(project_path, '.cursorrules')
        if not os.path.exists(cursorrules):
            os.symlink('CLAUDE.md', cursorrules)
            print("         .cursorrules -> CLAUDE.md")
    except:
        pass  # Symlinks opcionales
    
    # Fase 6: README.md
    print(f"\n  [6/6] Creando README.md...")
    readme_content = f"""# {project_name}

Sistema de optimización de contexto para agentes de IA instalado.

## Stack
- **Lenguajes**: {', '.join(languages)}
- **Backend**: {', '.join(frameworks['backend']) if frameworks['backend'] else 'N/A'}
- **Frontend**: {', '.join(frameworks['frontend']) if frameworks['frontend'] else 'N/A'}

## Estructura .ai/
Consulta `.ai/PROJECT_INDEX.yaml` para el mapa completo del proyecto.

Generado por **AI Agent Wizard v1.0.0**
"""
    
    readme_path = os.path.join(project_path, 'README.md')
    if not os.path.exists(readme_path):
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("         README.md")
    
    # Resumen
    show_warnings_summary()
    
    print(f"\n  {'=' * 60}")
    print(f"  INSTALACIÓN COMPLETADA")
    print(f"  {'=' * 60}")
    print(f"  Archivos indexados:  {len(files_map)}")
    print(f"  Funciones:           {total_funcs}")
    print(f"  Endpoints:           {len(endpoints)}")
    print(f"  Componentes:         {len(components)}")
    
    return True


def main():
    """Entry point principal"""
    print("\n  " + "=" * 60)
    print("  AI AGENT WIZARD v1.0.0")
    print("  Sistema de optimización de contexto para agentes de IA")
    print("  " + "=" * 60)
    
    # Parsear argumentos
    auto_mode = '--auto' in sys.argv
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    
    if '--help' in sys.argv or '-h' in sys.argv:
        print("""
  USO:
    python main.py [ruta_proyecto] [opciones]
  
  OPCIONES:
    --auto          Modo no interactivo
    --verbose, -v   Modo debug detallado
    --help, -h      Muestra esta ayuda
  
  EJEMPLOS:
    python main.py                   # Proyecto actual
    python main.py /path/proyecto    # Ruta específica
    python main.py --auto --verbose  # Auto + debug
        """)
        sys.exit(0)
    
    # Determinar ruta del proyecto
    args = [a for a in sys.argv[1:] if not a.startswith('--') and not a.startswith('-')]
    if args:
        project_path = args[0]
    else:
        project_path = os.getcwd()
    
    # Ejecutar instalación
    success = install(project_path, auto_mode=auto_mode, verbose=verbose)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
