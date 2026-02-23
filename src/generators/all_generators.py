"""
Generador consolidado de todos los archivos .ai/
Crea índices con acceso directo a funciones, eliminando navegación manual.
Importa funciones del instalador original para reutilización.
"""

import datetime
import os
from pathlib import Path


def generate_project_index(project_path, project_name, languages, frameworks, files_map,
                           functions, endpoints, components, dependencies):
    """Genera PROJECT_INDEX.yaml"""
    today = datetime.date.today().isoformat()

    lines = []
    lines.append("# " + "=" * 76)
    lines.append(f"# {project_name.upper()} - AI PROJECT INDEX")
    lines.append("# " + "=" * 76)
    lines.append(f"# LAST_UPDATED: {today}")
    lines.append("# " + "=" * 76)
    lines.append("")
    lines.append("meta:")
    lines.append(f"  name: {project_name}")
    lines.append(f"  desc: Proyecto con sistema .ai/ de AI Agent Wizard")
    lines.append(f"  lang: [{', '.join(languages)}]")
    lines.append("  stack:")
    if frameworks.get('backend'):
        lines.append(f"    backend: {', '.join(frameworks['backend'])}")
    if frameworks.get('frontend'):
        lines.append(f"    frontend: {', '.join(frameworks['frontend'])}")
    if frameworks.get('db'):
        lines.append(f"    db: [{', '.join(frameworks['db'])}]")
    lines.append(f"  root: {project_path}")
    lines.append("")

    # Files
    lines.append("# " + "=" * 76)
    lines.append("# FILE MAP")
    lines.append("# " + "=" * 76)
    lines.append("files:")
    for fpath in sorted(files_map.keys()):
        info = files_map[fpath]
        lines.append(f"  {fpath}:")
        lines.append(f"    type: {info['type']}")
        lines.append(f"    lines: ~{info['lines']}")
    lines.append("")

    # Functions
    if functions:
        lines.append("# " + "=" * 76)
        lines.append("# FUNCTIONS - name: line")
        lines.append("# " + "=" * 76)
        lines.append("functions:")
        for fpath in sorted(functions.keys()):
            lines.append(f"  {fpath}:")
            for func_name, line_num in sorted(functions[fpath].items(), key=lambda x: x[1]):
                lines.append(f"    {func_name}: {line_num}")
        lines.append("")

    # Endpoints
    if endpoints:
        lines.append("# " + "=" * 76)
        lines.append("# API ENDPOINTS")
        lines.append("# " + "=" * 76)
        lines.append("endpoints:")
        for ep_key in sorted(endpoints.keys()):
            ep = endpoints[ep_key]
            lines.append(f'  "{ep_key}": {{handler: {ep["handler"]}, file: {ep["file"]}, line: {ep["line"]}}}')
        lines.append("")

    # Components
    if components:
        lines.append("# " + "=" * 76)
        lines.append("# UI COMPONENTS")
        lines.append("# " + "=" * 76)
        lines.append("components:")
        for comp_name in sorted(components.keys()):
            comp = components[comp_name]
            lines.append(f"  {comp_name}:")
            lines.append(f"    file: {comp['file']}")
            if comp.get('props'):
                lines.append(f"    props: [{', '.join(comp['props'])}]")
            if comp.get('emits'):
                lines.append(f"    emits: [{', '.join(comp['emits'])}]")
        lines.append("")

    # Dependencies
    if dependencies:
        lines.append("# " + "=" * 76)
        lines.append("# DEPENDENCIES")
        lines.append(" # " + "=" * 76)
        lines.append("dependencies:")
        for fpath in sorted(dependencies.keys()):
            deps_list = ', '.join(dependencies[fpath])
            lines.append(f"  {fpath}: [{deps_list}]")
        lines.append("")
    
    return '\n'.join(lines) + '\n'


def generate_all_yamls(project_name, languages, frameworks, project_path=None, files_map=None):
    """Genera todos los YAMLs necesarios con información dinámica del proyecto"""
    today = datetime.date.today().isoformat()
    
    has_python = 'Python' in languages
    has_js = any('JavaScript' in l or 'TypeScript' in l for l in languages)
    has_php = 'PHP' in languages
    
    yamls = {}
    
    # CONVENTIONS.yaml
    yamls['CONVENTIONS.yaml'] = f"""# {project_name} Conventions
# Last Updated: {today}

naming:
  {'files_python: snake_case.py' if has_python else ''}
  {'functions_python: snake_case' if has_python else ''}
  {'files_javascript: camelCase.js' if has_js else ''}
  css_classes: kebab-case

code_style:
  indentation: "4 spaces"
  max_line_length: 120
"""
    
    # TESTING.yaml — Detectar test runners del proyecto
    backend_fw = frameworks.get('backend', [])
    test_commands = []
    test_config_files = []
    
    # Detectar configuración de testing
    if project_path:
        test_configs = {
            'pytest.ini': 'pytest',
            'setup.cfg': 'pytest',
            'tox.ini': 'tox',
            'jest.config.js': 'jest',
            'jest.config.ts': 'jest',
            'vitest.config.js': 'vitest',
            'vitest.config.ts': 'vitest',
            'karma.conf.js': 'karma',
            'cypress.config.js': 'cypress',
            'cypress.config.ts': 'cypress',
            'playwright.config.ts': 'playwright',
            'phpunit.xml': 'phpunit',
            'phpunit.xml.dist': 'phpunit',
        }
        for config_file, runner in test_configs.items():
            if os.path.exists(os.path.join(project_path, config_file)):
                test_config_files.append(f"  config: {config_file} ({runner})")
    
    # Determinar comandos de test
    if any('pytest' in f.lower() or 'python' in f.lower() or 'django' in f.lower() for f in backend_fw):
        test_commands.append('  unit: "pytest tests/ -v"')
        if any('django' in f.lower() for f in backend_fw):
            test_commands.append('  django: "python manage.py test"')
    if has_js:
        test_commands.append('  unit_js: "npm test"')
    if has_php:
        test_commands.append('  unit_php: "vendor/bin/phpunit"')
    if not test_commands:
        test_commands.append('  unit: "pytest tests/ -v"' if has_python else '  unit: "npm test"')
    
    # Detectar directorio de tests
    test_dirs = []
    if project_path:
        for td in ['tests', 'test', '__tests__', 'spec', 'tests/unit', 'tests/integration']:
            if os.path.isdir(os.path.join(project_path, td)):
                test_dirs.append(td)
    
    testing_yaml = f"""# {project_name} Testing
# Last Updated: {today}

test_commands:
{chr(10).join(test_commands)}
"""
    if test_dirs:
        testing_yaml += f"""
test_directories:
"""
        for td in test_dirs:
            testing_yaml += f"  - {td}\n"
    
    if test_config_files:
        testing_yaml += f"""
detected_config:
{chr(10).join(test_config_files)}
"""
    
    yamls['TESTING.yaml'] = testing_yaml
    
    # ERRORS.yaml — Detectar patrones de error del proyecto
    error_lines = [f"# {project_name} Common Errors", f"# Last Updated: {today}", ""]
    error_lines.append("common_errors:")
    
    # Analizar patterns de error del código fuente
    error_patterns_found = set()
    if files_map:
        import re as _re
        for fpath, info in files_map.items():
            ext = info['type']
            content_lines = info.get('content', [])
            for line in content_lines:
                # Python: except XxxError
                if ext == 'py':
                    m = _re.search(r'except\s+(\w*Error|\w*Exception)', line)
                    if m:
                        error_patterns_found.add(m.group(1))
                # JS/TS: catch (error)
                elif ext in ('js', 'ts', 'tsx', 'jsx'):
                    if 'throw new' in line:
                        m = _re.search(r'throw\s+new\s+(\w+)', line)
                        if m:
                            error_patterns_found.add(m.group(1))
                # PHP: catch (Exception $e)
                elif ext == 'php':
                    m = _re.search(r'catch\s*\(\s*(\w+)', line)
                    if m:
                        error_patterns_found.add(m.group(1))
    
    if error_patterns_found:
        for pattern in sorted(error_patterns_found):
            error_lines.append(f'  - pattern: "{pattern}"')
            error_lines.append(f'    source: "project code"')
    
    # Agregar errores comunes según el stack
    if has_python:
        error_lines.append('  - pattern: "ModuleNotFoundError"')
        error_lines.append('    cause: "Missing dependency"')
        error_lines.append('    fix: "pip install <package>"')
        error_lines.append('  - pattern: "ImportError"')
        error_lines.append('    cause: "Circular import or missing module"')
        error_lines.append('    fix: "Check import order and dependencies"')
    if has_js:
        error_lines.append('  - pattern: "Cannot find module"')
        error_lines.append('    cause: "Missing npm package"')
        error_lines.append('    fix: "npm install <package>"')
        error_lines.append('  - pattern: "TypeError: X is not a function"')
        error_lines.append('    cause: "Wrong import or undefined method"')
        error_lines.append('    fix: "Check exports and import paths"')
    if has_php:
        error_lines.append('  - pattern: "Class not found"')
        error_lines.append('    cause: "Missing autoload or namespace"')
        error_lines.append('    fix: "composer dump-autoload"')
    
    error_lines.append("")
    yamls['ERRORS.yaml'] = '\n'.join(error_lines)
    
    # GIT_WORKFLOW.yaml
    yamls['GIT_WORKFLOW.yaml'] = f"""# {project_name} Git Workflow
# Last Updated: {today}

repository:
  main_branch: main
  current_version: v0.1.0

commit_policy:
  format: conventional_commits
  types:
    feat: New feature
    fix: Bug fix
    refactor: Code refactor
    test: Tests
    chore: Maintenance
"""
    
    return yamls


def generate_architecture_yaml(project_path, languages=None, frameworks=None, 
                               files_map=None, functions=None, dependencies=None):
    """Genera ARCHITECTURE.yaml dinámico analizando la estructura real del proyecto"""
    project_name = os.path.basename(project_path)
    today = datetime.date.today().isoformat()
    
    lines = []
    lines.append(f"# {project_name.upper()} - PROJECT ARCHITECTURE")
    lines.append(f"# Generated: {today}")
    lines.append(f"# Understand the project structure and execution flow")
    lines.append("")
    
    # Propósito del sistema .ai/
    lines.append("optimizer_purpose: |")
    lines.append("  This .ai/ system was created to help AI agents understand your project efficiently.")
    lines.append("  It maps code structure so every function, endpoint, and component is immediately accessible.")
    lines.append("  Read PROJECT_INDEX.yaml for the complete map. Read FLOW.yaml for usage instructions.")
    lines.append("")
    
    # Detectar estructura de directorios principales
    lines.append("# " + "=" * 60)
    lines.append("# DIRECTORY STRUCTURE")
    lines.append("# " + "=" * 60)
    lines.append("directories:")
    
    if files_map:
        # Extraer directorios únicos de primer y segundo nivel
        dirs_count = {}
        for fpath in files_map:
            parts = fpath.replace("\\", "/").split("/")
            if len(parts) > 1:
                top_dir = parts[0]
                if top_dir not in dirs_count:
                    dirs_count[top_dir] = {"files": 0, "subdirs": set()}
                dirs_count[top_dir]["files"] += 1
                if len(parts) > 2:
                    dirs_count[top_dir]["subdirs"].add(parts[1])
            
        for d in sorted(dirs_count.keys()):
            info = dirs_count[d]
            subdirs_str = f", subdirs: [{', '.join(sorted(info['subdirs']))}]" if info['subdirs'] else ""
            lines.append(f"  {d}/: {{files: {info['files']}{subdirs_str}}}")
    else:
        # Fallback: escanear directorio
        try:
            for item in sorted(os.listdir(project_path)):
                item_path = os.path.join(project_path, item)
                if os.path.isdir(item_path) and not item.startswith('.') and item not in {
                    'node_modules', '__pycache__', '.git', 'venv', '.venv', 'dist', 'build'
                }:
                    file_count = sum(1 for _ in Path(item_path).rglob('*') if _.is_file())
                    lines.append(f"  {item}/: {{files: ~{file_count}}}")
        except Exception:
            lines.append("  # No se pudo analizar la estructura")
    lines.append("")
    
    # Stack tecnológico
    if languages or frameworks:
        lines.append("# " + "=" * 60)
        lines.append("# TECHNOLOGY STACK")
        lines.append("# " + "=" * 60)
        lines.append("stack:")
        if languages:
            lines.append(f"  languages: [{', '.join(languages)}]")
        if frameworks:
            if frameworks.get('backend'):
                lines.append(f"  backend: [{', '.join(frameworks['backend'])}]")
            if frameworks.get('frontend'):
                lines.append(f"  frontend: [{', '.join(frameworks['frontend'])}]")
            if frameworks.get('db'):
                lines.append(f"  database: [{', '.join(frameworks['db'])}]")
            if frameworks.get('other'):
                lines.append(f"  infrastructure: [{', '.join(frameworks['other'])}]")
        lines.append("")
    
    # Módulos principales con sus funciones
    if functions:
        lines.append("# " + "=" * 60)
        lines.append("# MODULE MAP - Key modules and their roles")
        lines.append("# " + "=" * 60)
        lines.append("modules:")
        
        # Agrupar por directorio de primer nivel
        module_groups = {}
        for fpath, funcs in functions.items():
            parts = fpath.replace("\\", "/").split("/")
            group = parts[0] if len(parts) > 1 else "(root)"
            if group not in module_groups:
                module_groups[group] = {}
            module_groups[group][fpath] = funcs
        
        for group in sorted(module_groups.keys()):
            lines.append(f"  # --- {group}/ ---")
            for fpath in sorted(module_groups[group].keys()):
                funcs = module_groups[group][fpath]
                func_names = sorted(funcs.keys())
                preview = func_names[:5]
                extra = f" (+{len(func_names)-5} more)" if len(func_names) > 5 else ""
                lines.append(f"  {fpath}:")
                lines.append(f"    functions: [{', '.join(preview)}{extra}]")
            lines.append("")
    
    # Dependencias entre módulos
    if dependencies:
        lines.append("# " + "=" * 60)
        lines.append("# MODULE DEPENDENCIES")
        lines.append("# " + "=" * 60)
        lines.append("dependencies:")
        for fpath in sorted(dependencies.keys()):
            deps_list = ', '.join(sorted(dependencies[fpath]))
            lines.append(f"  {fpath}: [{deps_list}]")
        lines.append("")
    
    # Detección de entry points
    lines.append("# " + "=" * 60)
    lines.append("# ENTRY POINTS & KEY CONCEPTS")
    lines.append("# " + "=" * 60)
    lines.append("entry_points:")
    
    # Buscar archivos comunes de entry point
    entry_files = []
    if files_map:
        for fpath in files_map:
            basename = os.path.basename(fpath).lower()
            if basename in ('main.py', 'app.py', 'index.js', 'index.ts', 'server.js', 
                           'server.ts', 'manage.py', 'wsgi.py', 'asgi.py', 'main.go',
                           'main.rs', 'Program.cs', 'Main.java'):
                entry_files.append(fpath)
    
    if entry_files:
        for ef in sorted(entry_files):
            lines.append(f"  - {ef}")
    else:
        lines.append("  - # No entry points detected automatically")
    lines.append("")
    
    # Instrucciones de regeneración
    lines.append("# " + "=" * 60)
    lines.append("# REGENERATING INDEXES")
    lines.append("# " + "=" * 60)
    lines.append("regenerate: |")
    lines.append("  After you modify code locally:")
    lines.append("    python .ai/update_index.py")
    lines.append("  ")
    lines.append("  When you want latest features from GitHub:")
    lines.append("    python .ai/update.py --auto")
    lines.append("  ")
    lines.append("  Both automatically regenerate all indexes.")
    lines.append("")
    
    return '\n'.join(lines) + '\n'


def generate_flow_yaml():
    """Genera FLOW.yaml con instrucciones para agentes IA sobre cómo usar los índices"""
    return """# AI AGENT EXECUTION FLOW
# How to use the .ai/ index system for efficient code comprehension

## STEP 1: UNDERSTAND PROJECT CONTEXT (READ FIRST)
read_order:
  1. this_file: "FLOW.yaml"
    why: Understand how to use the index system efficiently
    time: 1 min
    
  2. PROJECT_INDEX.yaml:
    why: Get complete project map (files, functions, endpoints, components)
    format: "YAML with exact line numbers"
    time: 2-3 min scan
    
  3. ARCHITECTURE.yaml:
    why: Understand project flow, modules, and how they connect
    format: "Natural language + structure"
    time: 2-3 min read

## STEP 2: LOCATE CODE YOU NEED
use_index_system: |
  NEVER scan entire files or guess locations.
  
  Instead:
  1. Read .ai/PROJECT_INDEX.yaml
  2. Find function/endpoint/component name
  3. Note the exact line number provided
  4. Use line number to jump directly to relevant code
  
  Example:
    Looking for handleClick function?
    - Search PROJECT_INDEX.yaml for "handleClick"
    - It shows: "handleClick: 245" in file src/components/Button.vue
    - Jump directly to line 245 in that file
    - Read only the relevant section, not entire file

## STEP 3: UNDERSTAND RELATIONSHIPS
module_flow: |
  For complex logic, understand module relationships:
  
  1. Read ARCHITECTURE.yaml for module dependency graph
  2. Trace the flow: how modules call each other
  3. Jump to specific functions using PROJECT_INDEX.yaml
  4. Never read entire modules, only functions you need

## STEP 4: FIND API ENDPOINTS
endpoints: |
  Need to understand an API route?
  
  1. Open PROJECT_INDEX.yaml 
  2. Look for "endpoints:" section
  3. Find your endpoint (e.g. "POST /api/users")
  4. Note the handler function and line number
  5. Jump directly to that handler

## STEP 5: LOCATE UI COMPONENTS
components: |
  Working with UI components?
  
  1. Open PROJECT_INDEX.yaml
  2. Look for "components:" section
  3. Find component name and file path
  4. Note props and emits
  5. Jump to exact line in component file

## TOKEN OPTIMIZATION RULES
rules:
  dont: [
    "Read entire files unless absolutely necessary",
    "Search manually through project structure",
    "Open files to find functions",
    "Browse directories to understand flow"
  ]
  
  do: [
    "Use PROJECT_INDEX.yaml as your map",
    "Jump directly to line numbers",
    "Read only relevant code sections",
    "Reference ARCHITECTURE.yaml for flow"
  ]

## AFTER CODE CHANGES
update_indexes: |
  When the developer modifies code:
  
  1. They run: python .ai/update_index.py
  2. All .ai/*.yaml files are regenerated
  3. New functions/endpoints appear in indexes
  4. You can immediately reference updated code
  
  Changes flow:
    code_changed → update_index.py → PROJECT_INDEX updated
    
## UNDERSTANDING .ai/ FILES
file_guide:
  PROJECT_INDEX.yaml: "Master index - functions, files, endpoints, components, dependencies"
  ARCHITECTURE.yaml: "Project structure - modules, flow, purpose, how everything connects"
  CONVENTIONS.yaml: "Code style - naming, indentation, patterns"
  TESTING.yaml: "How to test - test commands, validation"
  ERRORS.yaml: "Common problems - known issues and fixes"
  GIT_WORKFLOW.yaml: "Git rules - branches, commits, versioning"
  
## EFFICIENCY EXAMPLE
example: |
  WRONG WAY (High Token Usage):
    1. Read entire project README
    2. Open src/main.py and read 200 lines
    3. Search through functions manually
    4. Finally find the function you need
    → 200+ lines read, high token cost
  
  RIGHT WAY (Optimized):
    1. Search PROJECT_INDEX.yaml for function name: function_x: 45
    2. Open file src/main.py
    3. Jump to line 45
    4. Read only 10-20 relevant lines
    → 20 lines read, 90% fewer tokens
"""

def generate_graph_yaml(dependencies, functions, endpoints, components):
    """Genera GRAPH.yaml - mapa comprimido de dependencias y relaciones reales del proyecto"""
    today = datetime.date.today().isoformat()
    total_funcs = sum(len(v) for v in functions.values()) if functions else 0
    total_deps = len(dependencies) if dependencies else 0
    total_eps = len(endpoints) if endpoints else 0
    total_comps = len(components) if components else 0
    
    lines = []
    lines.append("# DEPENDENCY GRAPH - Compressed module relationships")
    lines.append(f"# Generated: {today}")
    lines.append("# Quick visual reference for understanding code flow")
    lines.append("")
    
    # Estadísticas
    lines.append("statistics:")
    lines.append(f"  total_functions: {total_funcs}")
    lines.append(f"  total_endpoints: {total_eps}")
    lines.append(f"  total_components: {total_comps}")
    lines.append(f"  files_with_dependencies: {total_deps}")
    lines.append("")
    
    # Grafo de dependencias real
    if dependencies:
        lines.append("# " + "=" * 60)
        lines.append("# MODULE DEPENDENCIES (who imports whom)")
        lines.append("# " + "=" * 60)
        lines.append("module_graph:")
        
        # Construir grafo simplificado por módulo (directorio)
        module_deps = {}
        for fpath, deps in dependencies.items():
            # Simplificar a directorio de primer nivel
            src_module = fpath.replace("\\", "/").split("/")[0] if "/" in fpath.replace("\\", "/") else "(root)"
            if src_module not in module_deps:
                module_deps[src_module] = set()
            for dep in deps:
                dep_module = dep.replace("\\", "/").split("/")[0] if "/" in dep.replace("\\", "/") else "(root)"
                if dep_module != src_module:
                    module_deps[src_module].add(dep_module)
        
        for mod in sorted(module_deps.keys()):
            targets = sorted(module_deps[mod])
            if targets:
                lines.append(f"  {mod}: [{', '.join(targets)}]")
            else:
                lines.append(f"  {mod}: []")
        lines.append("")
        
        # Dependencias detalladas archivo a archivo
        lines.append("# " + "=" * 60)
        lines.append("# FILE-LEVEL DEPENDENCIES (detailed)")
        lines.append("# " + "=" * 60)
        lines.append("file_dependencies:")
        for fpath in sorted(dependencies.keys()):
            deps_list = ', '.join(sorted(dependencies[fpath]))
            lines.append(f"  {fpath}: [{deps_list}]")
        lines.append("")
    
    # Endpoints como puntos de entrada
    if endpoints:
        lines.append("# " + "=" * 60)
        lines.append("# API ENTRY POINTS")
        lines.append("# " + "=" * 60)
        lines.append("api_routes:")
        for ep_key in sorted(endpoints.keys()):
            ep = endpoints[ep_key]
            lines.append(f'  "{ep_key}": {{handler: {ep["handler"]}, file: {ep["file"]}, line: {ep["line"]}}}')
        lines.append("")
    
    # Componentes como nodos UI
    if components:
        lines.append("# " + "=" * 60)
        lines.append("# UI COMPONENT TREE")
        lines.append("# " + "=" * 60)
        lines.append("component_graph:")
        for comp_name in sorted(components.keys()):
            comp = components[comp_name]
            props_str = f", props: [{', '.join(comp['props'])}]" if comp.get('props') else ""
            emits_str = f", emits: [{', '.join(comp['emits'])}]" if comp.get('emits') else ""
            lines.append(f"  {comp_name}: {{file: {comp['file']}{props_str}{emits_str}}}")
        lines.append("")
    
    # Archivos más conectados (hubs)
    if functions:
        lines.append("# " + "=" * 60)
        lines.append("# KEY FILES (most functions)")
        lines.append("# " + "=" * 60)
        lines.append("key_files:")
        sorted_files = sorted(functions.items(), key=lambda x: len(x[1]), reverse=True)
        for fpath, funcs in sorted_files[:10]:
            lines.append(f"  {fpath}: {len(funcs)} functions")
        lines.append("")
    
    # Instrucciones de uso
    lines.append("# " + "=" * 60)
    lines.append("# HOW TO USE THIS GRAPH")
    lines.append("# " + "=" * 60)
    lines.append("usage: |")
    lines.append("  1. Check module_graph for high-level module relationships")
    lines.append("  2. Check file_dependencies for specific file imports")
    lines.append("  3. Check api_routes for endpoint entry points")
    lines.append("  4. Check key_files for the most important files")
    lines.append("  5. Use PROJECT_INDEX.yaml to jump to specific functions by line number")
    lines.append("")
    
    return '\n'.join(lines) + '\n'


def generate_changes_yaml(project_path, files_map):
    """
    Genera CHANGES.yaml — indexación sensible a cambios.
    Calcula hash MD5 de cada archivo fuente y lo compara con el estado anterior
    guardado en .ai/.state.json para identificar archivos modificados.
    """
    import hashlib
    import json as _json
    
    today = datetime.date.today().isoformat()
    ai_dir = os.path.join(project_path, '.ai')
    state_file = os.path.join(ai_dir, '.state.json')
    
    # Cargar estado anterior
    prev_state = {}
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                prev_state = _json.load(f)
        except Exception:
            prev_state = {}
    
    # Calcular hashes actuales
    current_state = {}
    changed = []
    added = []
    unchanged = []
    
    for fpath, info in files_map.items():
        # Calcular hash del contenido
        if 'content' in info and info['content']:
            content_str = ''.join(info['content'])
        else:
            # Si content ya fue liberado, leer archivo
            full_path = os.path.join(project_path, fpath)
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content_str = f.read()
            except Exception:
                continue
        
        file_hash = hashlib.md5(content_str.encode('utf-8', errors='ignore')).hexdigest()
        current_state[fpath] = file_hash
        
        if fpath not in prev_state:
            added.append(fpath)
        elif prev_state[fpath] != file_hash:
            changed.append(fpath)
        else:
            unchanged.append(fpath)
    
    # Archivos eliminados
    removed = [f for f in prev_state if f not in current_state]
    
    # Guardar estado actual
    os.makedirs(ai_dir, exist_ok=True)
    try:
        with open(state_file, 'w', encoding='utf-8') as f:
            _json.dump(current_state, f, indent=2)
    except Exception:
        pass
    
    # Generar YAML
    lines = []
    lines.append("# CHANGES - Change-Aware Index")
    lines.append(f"# Generated: {today}")
    lines.append("# Tracks which files have changed since last indexing")
    lines.append("")
    lines.append("summary:")
    lines.append(f"  total_files: {len(current_state)}")
    lines.append(f"  changed: {len(changed)}")
    lines.append(f"  added: {len(added)}")
    lines.append(f"  removed: {len(removed)}")
    lines.append(f"  unchanged: {len(unchanged)}")
    lines.append("")
    
    if changed:
        lines.append("# Files modified since last index")
        lines.append("changed_files:")
        for f in sorted(changed):
            lines.append(f"  - {f}")
        lines.append("")
    
    if added:
        lines.append("# New files since last index")
        lines.append("added_files:")
        for f in sorted(added):
            lines.append(f"  - {f}")
        lines.append("")
    
    if removed:
        lines.append("# Files removed since last index")
        lines.append("removed_files:")
        for f in sorted(removed):
            lines.append(f"  - {f}")
        lines.append("")
    
    lines.append("# USAGE: Focus attention on changed_files and added_files")
    lines.append("# These are the files most likely needing review")
    lines.append("")
    
    return '\n'.join(lines) + '\n'


def generate_summaries_yaml(files_map, functions):
    """
    Genera SUMMARIES.yaml — resúmenes semánticos de 1-2 líneas por archivo.
    Extrae docstrings, comentarios iniciales y nombres de funciones
    para crear un resumen automático de cada módulo.
    """
    import re as _re
    today = datetime.date.today().isoformat()
    
    lines = []
    lines.append("# SUMMARIES - Semantic File Descriptions")
    lines.append(f"# Generated: {today}")
    lines.append("# One-line summary per file for quick project understanding")
    lines.append("")
    lines.append("files:")
    
    for fpath in sorted(files_map.keys()):
        info = files_map[fpath]
        summary = _extract_file_summary(fpath, info, functions)
        lines.append(f"  {fpath}: \"{summary}\"")
    
    lines.append("")
    return '\n'.join(lines) + '\n'


def _extract_file_summary(fpath, info, functions):
    """Extrae resumen semántico de un archivo basado en docstrings y nombres."""
    ext = info['type']
    content_lines = info.get('content', [])
    
    if not content_lines:
        return f"{ext} file (~{info.get('lines', 0)} lines)"
    
    # Intentar extraer docstring/comentario inicial
    summary = ""
    
    if ext == 'py':
        # Buscar docstring del módulo (triple quotes)
        joined = ''.join(content_lines[:20])
        import re as _re
        doc_match = _re.search(r'"""(.*?)"""', joined, _re.DOTALL)
        if not doc_match:
            doc_match = _re.search(r"'''(.*?)'''", joined, _re.DOTALL)
        if doc_match:
            summary = doc_match.group(1).strip().split('\n')[0].strip()
        else:
            # Buscar comentario # al inicio
            for line in content_lines[:5]:
                stripped = line.strip()
                if stripped.startswith('#') and not stripped.startswith('#!'):
                    summary = stripped.lstrip('#').strip()
                    break
    
    elif ext in ('js', 'ts', 'tsx', 'jsx'):
        # Buscar comentario /** */ o //
        joined = ''.join(content_lines[:15])
        import re as _re
        doc_match = _re.search(r'/\*\*\s*(.*?)\*/', joined, _re.DOTALL)
        if doc_match:
            first_line = doc_match.group(1).strip().split('\n')[0]
            summary = first_line.lstrip('* ').strip()
        else:
            for line in content_lines[:5]:
                stripped = line.strip()
                if stripped.startswith('//') and not stripped.startswith('///'):
                    summary = stripped.lstrip('/').strip()
                    break
    
    elif ext == 'php':
        joined = ''.join(content_lines[:15])
        import re as _re
        doc_match = _re.search(r'/\*\*\s*(.*?)\*/', joined, _re.DOTALL)
        if doc_match:
            first_line = doc_match.group(1).strip().split('\n')[0]
            summary = first_line.lstrip('* ').strip()
    
    # Si no hay docstring, usar nombres de funciones
    if not summary and fpath in functions:
        func_names = list(functions[fpath].keys())[:4]
        summary = f"Contains: {', '.join(func_names)}"
        if len(functions[fpath]) > 4:
            summary += f" (+{len(functions[fpath]) - 4} more)"
    
    # Fallback
    if not summary:
        summary = f"{ext} file (~{info.get('lines', 0)} lines)"
    
    # Truncar a 120 caracteres
    if len(summary) > 120:
        summary = summary[:117] + "..."
    
    # Escapar comillas dobles para YAML
    summary = summary.replace('"', '\\"')
    
    return summary


def generate_context_budget_yaml(files_map, functions, endpoints, components):
    """
    Genera CONTEXT_BUDGET.yaml — jerarquía de 3 niveles para optimización de tokens.
    Clasifica archivos en niveles de prioridad para lectura eficiente.
    """
    today = datetime.date.today().isoformat()
    
    # Clasificar archivos por importancia
    critical = []   # Entry points, rutas principales, configs
    important = []   # Módulos con muchas funciones, controllers
    reference = []   # Utilidades, tests, assets
    
    for fpath, info in files_map.items():
        basename = os.path.basename(fpath).lower()
        ext = info['type']
        func_count = len(functions.get(fpath, {}))
        has_endpoints = any(ep['file'] == fpath for ep in endpoints.values()) if endpoints else False
        has_components = any(comp['file'] == fpath for comp in components.values()) if components else False
        
        # Level 1: Critical (entry points, routes, main configs)
        if basename in ('main.py', 'app.py', 'index.js', 'index.ts', 'server.js', 'server.ts',
                        'manage.py', 'wsgi.py', 'asgi.py', 'main.go', 'main.rs',
                        'routes.py', 'urls.py', 'web.php', 'api.php'):
            critical.append((fpath, func_count, info.get('lines', 0)))
        elif has_endpoints:
            critical.append((fpath, func_count, info.get('lines', 0)))
        # Level 2: Important (many functions, components, models)
        elif func_count >= 5 or has_components:
            important.append((fpath, func_count, info.get('lines', 0)))
        elif 'model' in basename or 'controller' in basename or 'service' in basename:
            important.append((fpath, func_count, info.get('lines', 0)))
        # Level 3: Reference
        else:
            reference.append((fpath, func_count, info.get('lines', 0)))
    
    lines = []
    lines.append("# CONTEXT BUDGET - Token Optimization Hierarchy")
    lines.append(f"# Generated: {today}")
    lines.append("# Read files in priority order to minimize token usage")
    lines.append("")
    lines.append("# Level 1: CRITICAL - Read these first (entry points, routes)")
    lines.append(f"# {len(critical)} files - read full context")
    lines.append("critical:")
    for fpath, fc, lc in sorted(critical, key=lambda x: -x[1]):
        lines.append(f"  - {{file: \"{fpath}\", functions: {fc}, lines: {lc}}}")
    lines.append("")
    
    lines.append("# Level 2: IMPORTANT - Read when relevant (core modules)")
    lines.append(f"# {len(important)} files - read key sections only")
    lines.append("important:")
    for fpath, fc, lc in sorted(important, key=lambda x: -x[1]):
        lines.append(f"  - {{file: \"{fpath}\", functions: {fc}, lines: {lc}}}")
    lines.append("")
    
    lines.append("# Level 3: REFERENCE - Read only when needed (utils, tests)")
    lines.append(f"# {len(reference)} files - scan briefly or skip")
    lines.append("reference:")
    for fpath, fc, lc in sorted(reference, key=lambda x: -x[1]):
        lines.append(f"  - {{file: \"{fpath}\", functions: {fc}, lines: {lc}}}")
    lines.append("")
    
    lines.append("# STRATEGY:")
    lines.append("# 1. Always read CRITICAL files first")
    lines.append("# 2. Read IMPORTANT files when working on related features")
    lines.append("# 3. Only read REFERENCE files when specifically needed")
    lines.append("# 4. Use PROJECT_INDEX.yaml line numbers to read specific sections, not whole files")
    lines.append("")
    
    return '\n'.join(lines) + '\n'


def generate_protocol_yaml():
    """
    Genera PROTOCOL.yaml — reglas de comportamiento para agentes IA.
    Define orden de lectura, reglas de modificación, y coordinación multi-agente.
    """
    return """# PROTOCOL - AI Agent Behavior Rules
# Rules for efficient and safe interaction with this codebase

## IDENTITY
identity: |
  You are working on a project with an AI-optimized indexing system (.ai/).
  This system was installed to help you work efficiently.
  Follow these rules to minimize token usage and avoid errors.

## READ ORDER (MANDATORY)
read_order:
  1_flow: ".ai/FLOW.yaml → Understand how to use the index system"
  2_index: ".ai/PROJECT_INDEX.yaml → Get the complete code map"
  3_arch: ".ai/ARCHITECTURE.yaml → Understand project structure"
  4_budget: ".ai/CONTEXT_BUDGET.yaml → Know which files matter most"
  5_changes: ".ai/CHANGES.yaml → See what changed recently"
  6_graph: ".ai/GRAPH.yaml → Understand module dependencies"

## MODIFICATION RULES
modification_rules:
  never_modify:
    - ".ai/*.yaml (auto-generated, will be overwritten)"
    - ".ai/src/ (indexing engine, do not touch)"
    - ".ai/update.py (updater script)"
    - ".ai/update_index.py (re-indexer script)"
  
  after_modifying_code:
    - "Run: python .ai/update_index.py"
    - "Or suggest the user run it"
    - "Check CHANGES.yaml for affected files"

## TOKEN OPTIMIZATION
token_rules:
  - "NEVER read entire files unless absolutely necessary"
  - "Use PROJECT_INDEX.yaml line numbers to read specific sections"
  - "Read CONTEXT_BUDGET.yaml to prioritize which files to read"
  - "Check SUMMARIES.yaml for a quick overview of any file"
  - "For dependencies, read GRAPH.yaml instead of scanning imports"

## MULTI-AGENT COORDINATION
multi_agent:
  - "Each agent should read PROTOCOL.yaml first"
  - "Check CHANGES.yaml before modifying any file"
  - "Coordinate through file comments, not direct communication"
  - "One agent per file at a time to avoid conflicts"
  - "After modifications, suggest running update_index.py"

## ERROR HANDLING
error_handling:
  - "If .ai/ is missing or corrupted, suggest: python .ai/update.py --auto"
  - "If indexes are stale, suggest: python .ai/update_index.py"
  - "If a function isn't in the index, it may be new — search the file directly"
  - "Check ERRORS.yaml for known project-specific errors"

## COMMIT GUIDELINES
commit_rules:
  - "Read GIT_WORKFLOW.yaml for project commit conventions"
  - "Include .ai/*.yaml in commits (they should be version-controlled)"
  - "The pre-commit hook auto-updates indexes before each commit"
"""