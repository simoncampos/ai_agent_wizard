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

## ⛔ STEP 0: CONTEXT ANCHOR (ALWAYS READ FIRST — EVERY SESSION)
context_anchor:
  file: ".ai/CONTEXT_ANCHOR.yaml"
  why: "Ultra-compact project summary (<25 lines). Read this EVERY time you start or resume work."
  when_to_reread:
    - "At the start of every conversation"
    - "Every 5 messages during a long conversation"
    - "When you feel unsure about the project's purpose or structure"
    - "After any context window compression or summarization"
  rule: "If you can only read ONE file, read CONTEXT_ANCHOR.yaml"

## STEP 1: UNDERSTAND PROJECT CONTEXT (READ ON FIRST SESSION)
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
  CONTEXT_ANCHOR.yaml: "Ultra-compact summary — read every session and every 5 messages"
  PROJECT_INDEX.yaml: "Master index - functions, files, endpoints, components, dependencies"
  ARCHITECTURE.yaml: "Project structure - modules, flow, purpose, how everything connects"
  CALL_GRAPH.yaml: "Function call relationships - who calls whom"
  TYPES.yaml: "Data models, interfaces, structs with their fields"
  DOCSTRINGS.yaml: "Function documentation - params, returns, descriptions"
  CONFIG_MAP.yaml: "Environment variables and configuration files"
  ENTRY_POINTS.yaml: "Boot sequence, request lifecycle, read order"
  PATTERNS.yaml: "Design patterns, middleware, auth, naming conventions"
  QUICK_CONTEXT.yaml: "Pre-computed answers for common tasks (add endpoint, add test, etc.)"
  CONVENTIONS.yaml: "Code style - naming, indentation, patterns"
  TESTING.yaml: "How to test - test commands, validation"
  ERRORS.yaml: "Common problems - known issues and fixes"
  GIT_WORKFLOW.yaml: "Git rules - branches, commits, versioning"
  
## CONTEXT PERSISTENCE RULES
context_persistence: |
  ⛔ CRITICAL: These rules prevent context loss during long conversations.
  
  1. ALWAYS read CONTEXT_ANCHOR.yaml at conversation start
  2. RE-READ CONTEXT_ANCHOR.yaml every ~5 messages
  3. If conversation was summarized/compressed, IMMEDIATELY re-read:
     - CONTEXT_ANCHOR.yaml (20 lines, <500 tokens)
     - AGENT_GUIDE.md (if you lost project rules)
  4. When including this conversation in a summary, ALWAYS include:
     "REMEMBER: Re-read .ai/CONTEXT_ANCHOR.yaml before continuing"
  5. Before every action, verify: Do I know what project this is?
     If not → read CONTEXT_ANCHOR.yaml

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
    Incluye protocolo de persistencia de contexto.
    """
    return """# PROTOCOL - AI Agent Behavior Rules
# Rules for efficient and safe interaction with this codebase

## IDENTITY
identity: |
  You are working on a project with an AI-optimized indexing system (.ai/).
  This system was installed to help you work efficiently.
  Follow these rules to minimize token usage and avoid errors.

## ⛔ CONTEXT PERSISTENCE (NON-NEGOTIABLE)
context_persistence:
  on_conversation_start: |
    1. Read AGENT_GUIDE.md (full — project rules and context)
    2. Read .ai/CONTEXT_ANCHOR.yaml (ultra-compact project summary)
    3. Read .ai/AI_INSTRUCTIONS.yaml (flow, stack, considerations)
    4. Then proceed to FLOW.yaml → PROJECT_INDEX.yaml
  
  every_5_messages: |
    Re-read .ai/CONTEXT_ANCHOR.yaml (~20 lines, <500 tokens).
    This prevents context drift during long conversations.
    Cost: negligible. Benefit: maintains accuracy.
  
  on_new_task: |
    Before starting ANY new task:
    1. Re-read .ai/CONTEXT_ANCHOR.yaml
    2. Consult .ai/CONTEXT_BUDGET.yaml for file priorities
    3. Check .ai/QUICK_CONTEXT.yaml for pre-computed guidance
  
  on_context_doubt: |
    If you are unsure about ANY rule or project detail:
    → Re-read AGENT_GUIDE.md (full rules)
    → Re-read .ai/AI_INSTRUCTIONS.yaml (project-specific notes)
    NEVER guess. NEVER assume. Look it up.
  
  on_file_modification: |
    After editing code:
    → Consult .ai/PROJECT_INDEX.yaml to verify impact on other files
    → Check .ai/CALL_GRAPH.yaml to see what functions depend on what you changed
    → Suggest user runs: python .ai/update_index.py
  
  on_summary_or_compression: |
    If the conversation is summarized or compressed:
    → Your FIRST action must be: read .ai/CONTEXT_ANCHOR.yaml
    → Include in any summary: "REMEMBER: Re-read .ai/CONTEXT_ANCHOR.yaml"
  
  never_assume: |
    If you cannot find a function in your memory:
    → Search PROJECT_INDEX.yaml
    → If not there, search the file directly
    → NEVER invent function names, parameters, or line numbers

## READ ORDER (MANDATORY)
read_order:
  0_anchor: ".ai/CONTEXT_ANCHOR.yaml → Ultra-compact summary (EVERY session, every 5 msgs)"
  1_flow: ".ai/FLOW.yaml → Understand how to use the index system"
  2_index: ".ai/PROJECT_INDEX.yaml → Get the complete code map"
  3_arch: ".ai/ARCHITECTURE.yaml → Understand project structure"
  4_budget: ".ai/CONTEXT_BUDGET.yaml → Know which files matter most"
  5_changes: ".ai/CHANGES.yaml → See what changed recently"
  6_graph: ".ai/GRAPH.yaml → Understand module dependencies"
  7_quick: ".ai/QUICK_CONTEXT.yaml → Pre-computed guidance for common tasks"

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
    - "Check CALL_GRAPH.yaml for functions that depend on changed code"

## TOKEN OPTIMIZATION
token_rules:
  - "NEVER read entire files unless absolutely necessary"
  - "Use PROJECT_INDEX.yaml line numbers to read specific sections"
  - "Read CONTEXT_BUDGET.yaml to prioritize which files to read"
  - "Check SUMMARIES.yaml for a quick overview of any file"
  - "For dependencies, read GRAPH.yaml instead of scanning imports"
  - "For function docs, read DOCSTRINGS.yaml instead of reading the function"
  - "For data shapes, read TYPES.yaml instead of searching for model definitions"
  - "For common tasks, read QUICK_CONTEXT.yaml before exploring code"

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

## ⛔ WORKFLOW RULES — WHEN TO UPDATE INDEXES AND COMMIT
workflow:
  during_fixes: |
    When fixing bugs or making code corrections:
    - Do NOT run update_index.py after each change
    - Do NOT commit to git after each change  
    - Do NOT update AGENT_GUIDE.md business section for minor fixes
    - Focus ONLY on fixing the code
  
  when_to_update: |
    Update indexes and commit ONLY when:
    - The USER confirms the implementation works ("it works", "looks good", "approved")
    - The USER explicitly asks you to update indexes or commit
    - The USER asks you to review and test yourself, AND you confirm it works
    
  correct_sequence: |
    After user approves:
    1. Update AGENT_GUIDE.md business section if there were significant project changes
    2. Suggest: python .ai/update_index.py
    3. Suggest commit with descriptive message per GIT_WORKFLOW.yaml
    
  summary: "Implement → User tests → User approves → THEN update and commit"

## COMMIT GUIDELINES
commit_rules:
  - "Read GIT_WORKFLOW.yaml for project commit conventions"
  - "Include .ai/*.yaml in commits (they should be version-controlled)"
  - "The pre-commit hook auto-updates indexes before each commit"
  - "Do NOT commit during active fix/debug cycles — wait for user approval"

## FIRST RESPONSE OBLIGATION
first_response: |
  Before giving your FIRST response in a new conversation:
  1. Read AGENT_GUIDE.md
  2. Check if the "QUÉ ES ESTE PROYECTO" section says "PENDIENTE"
  3. If PENDIENTE: Complete it NOW using .ai/ indexes. Do NOT respond to user first.
  4. If already completed: Verify it's still accurate, update if needed.
  This ensures every agent understands the project before acting.

## CONTEXT CHECK (Quick Self-Test)
context_check: |
  Before every response, ask yourself:
  ✓ Did I complete the project description in AGENT_GUIDE.md?
    → If it says PENDIENTE: complete it NOW before anything else
  ✓ Do I know what this project is and what it does?
    → If not: read .ai/CONTEXT_ANCHOR.yaml
  ✓ Do I know where the code I need is located?
    → If not: read .ai/PROJECT_INDEX.yaml
  ✓ Do I know the project's rules and conventions?
    → If not: read .ai/PROTOCOL.yaml + AGENT_GUIDE.md
  ✓ Am I in fix/debug mode?
    → If yes: do NOT update indexes or commit
"""


def generate_ai_instructions(project_path, languages, frameworks, files_map, functions, endpoints, components):
    """
    Genera AI_INSTRUCTIONS.yaml — instrucciones dinámicas para agentes IA.
    
    Combina instrucciones genéricas (patrones, consideraciones) con información
    dinámicamente detectada del proyecto actual (lenguajes, frameworks, stack).
    
    Se regenera automáticamente con cada update_index.py para mantener instrucciones
    contextualizadas al estado actual del proyecto.
    
    Args:
        project_path: Ruta del proyecto
        languages: Lista de lenguajes detectados
        frameworks: Dict {'backend': [...], 'frontend': [...], 'db': [...]}
        files_map: Dict {filepath: {'type': 'py', 'lines': N}}
        functions: Dict {filepath: {func_name: line_num}}
        endpoints: Dict {endpoint_key: {'handler': name, 'file': path, 'line': N}}
        components: Dict {component_name: {'file': path, 'props': [...]}}
    
    Returns:
        String YAML con instrucciones completas
    """
    today = datetime.date.today().isoformat()
    
    # Estadísticas del proyecto
    total_files = len(files_map)
    total_functions = sum(len(v) for v in functions.values())
    total_endpoints = len(endpoints)
    total_components = len(components)
    total_lines = sum(f['lines'] for f in files_map.values())
    
    # Backend, frontend, DB
    backend_fw = frameworks.get('backend', [])
    frontend_fw = frameworks.get('frontend', [])
    db_fw = frameworks.get('db', [])
    other_fw = frameworks.get('other', [])
    
    # Detectar patrones especiales
    has_django = any('django' in f.lower() for f in backend_fw)
    has_flask = any('flask' in f.lower() for f in backend_fw)
    has_fastapi = any('fastapi' in f.lower() for f in backend_fw)
    has_react = any('react' in f.lower() for f in frontend_fw)
    has_vue = any('vue' in f.lower() for f in frontend_fw)
    has_nextjs = any('next' in f.lower() for f in frontend_fw)
    has_docker = any('docker' in f.lower() for f in other_fw)
    
    lines = []
    
    # ========================================================================
    # HEADER
    # ========================================================================
    lines.append("# " + "=" * 76)
    lines.append("# AI_INSTRUCTIONS - Instrucciones de Flujo para Agentes de IA")
    lines.append("# " + "=" * 76)
    lines.append(f"# GENERADO: {today} (Se actualiza automáticamente con update_index.py)")
    lines.append("# " + "=" * 76)
    lines.append("")
    
    # ========================================================================
    # METADATA
    # ========================================================================
    lines.append("meta:")
    lines.append(f"  description: Instrucciones dinámicas contextualizadas al proyecto actual")
    lines.append(f"  regenerated: '{today}'")
    lines.append(f"  when_regenerates: Al ejecutar 'python .ai/update_index.py' después de cambios")
    lines.append(f"  purpose: Guiar agentes IA sobre flujo, patrones y consideraciones específicas del proyecto")
    lines.append("")
    
    # ========================================================================
    # PROJECT STATISTICS
    # ========================================================================
    lines.append("# " + "=" * 76)
    lines.append("# PROJECT STATISTICS")
    lines.append("# " + "=" * 76)
    lines.append("statistics:")
    lines.append(f"  files_total: {total_files}")
    lines.append(f"  lines_of_code: ~{total_lines}")
    lines.append(f"  functions_classes: {total_functions}")
    lines.append(f"  api_endpoints: {total_endpoints}")
    lines.append(f"  ui_components: {total_components}")
    lines.append("")
    
    # ========================================================================
    # PROJECT FLOW
    # ========================================================================
    lines.append("# " + "=" * 76)
    lines.append("# PROJECT FLOW - 6 Fases del Sistema")
    lines.append("# " + "=" * 76)
    lines.append("flow:")
    lines.append("  phase_1_validation: |")
    lines.append("    Valida entorno (Python 3.7+, Git, permisos, espacio en disco)")
    lines.append("    No requiere intervención de IA")
    lines.append("")
    lines.append("  phase_2_scanning: |")
    lines.append("    Itera archivos fuente excluyendo dependencias (node_modules, venv, .git, etc.)")
    lines.append("    Construye files_map: {filepath: {type, lines}}")
    lines.append("    Soporta 31 extensiones de código (Python, JS, TS, Go, Rust, Java, PHP, C#, etc.)")
    lines.append("")
    lines.append("  phase_3_detection: |")
    lines.append("    Detecta lenguajes por extensión de archivo")
    lines.append("    Detecta frameworks por archivos de configuración (package.json, pyproject.toml, etc.)")
    lines.append("    Mapea stack en 4 categorías: backend, frontend, db, other")
    lines.append("")
    lines.append("  phase_4_extraction: |")
    lines.append("    Extrae información del código CON NÚMEROS DE LÍNEA EXACTOS (1-based)")
    lines.append("    • extract_functions(): Detecta def/class/fn/struct con decoradores")
    lines.append("    • extract_endpoints(): Identifica rutas REST (METHOD /route)")
    lines.append("    • extract_vue_components(): Detecta componentes UI")
    lines.append("    • extract_dependencies(): Mapea importaciones entre archivos")
    lines.append("")
    lines.append("  phase_5_memory_optimization: |")
    lines.append("    CRÍTICO: Libera contenido completo (lineas de código) tras extracción")
    lines.append("    Preserva solo: type, lines, funciones/endpoints/componentes")
    lines.append("    Reduce footprint de 100MB+ a <5MB para proyectos grandes")
    lines.append("")
    lines.append("  phase_6_generation: |")
    lines.append("    Genera 14 archivos YAML con índices y metadata")
    lines.append("    Copia motor de indexación a .ai/src/")
    lines.append("    Instala scripts de actualización y git hook automático")
    lines.append("")
    
    # ========================================================================
    # DATA STRUCTURES
    # ========================================================================
    lines.append("# " + "=" * 76)
    lines.append("# DATA STRUCTURES - Formatos Internos")
    lines.append("# " + "=" * 76)
    lines.append("data_structures:")
    lines.append("")
    lines.append("  files_map: |")
    lines.append("    Dict {filepath_relativo: {'type': extension, 'lines': count}}")
    lines.append("    Ejemplo:")
    lines.append("      'src/main.py': {'type': 'py', 'lines': 372}")
    lines.append("      'src/core/scanner.py': {'type': 'py', 'lines': 128}")
    lines.append("    Nota: Se libera 'content' (líneas) después de extracción para optimizar memoria")
    lines.append("")
    lines.append("  functions: |")
    lines.append("    Dict {filepath: {function_name: line_number (1-based)}}")
    lines.append("    Ejemplo:")
    lines.append("      'src/main.py':")
    lines.append("        install: 75")
    lines.append("        validate_environment: 180")
    lines.append("        _copy_tree_clean: 35")
    lines.append("    Convención clases:")
    lines.append("      'src/validators.py':")
    lines.append("        'DataValidator.validate': 120")
    lines.append("")
    lines.append("  endpoints: |")
    lines.append("    Dict {endpoint_key: {'handler': func, 'file': path, 'line': N}}")
    lines.append("    Ejemplo:")
    lines.append("      'GET /api/users': {'handler': 'get_users', 'file': 'src/routes/users.py', 'line': 45}")
    lines.append("      'POST /api/users': {'handler': 'create_user', 'file': 'src/routes/users.py', 'line': 60}")
    lines.append("")
    lines.append("  components: |")
    lines.append("    Dict {component_name: {'file': path, 'props': [...], 'emits': [...]}}")
    lines.append("    Ejemplo:")
    lines.append("      'UserCard': {'file': 'src/components/UserCard.vue', 'props': ['user', 'editable']}")
    lines.append("")
    
    # ========================================================================
    # DETECTED STACK (DINÁMICO)
    # ========================================================================
    lines.append("# " + "=" * 76)
    lines.append("# DETECTED STACK - Lo que se encontró en THIS proyecto")
    lines.append("# " + "=" * 76)
    lines.append("detected_stack:")
    lines.append(f"  languages: [{', '.join(languages)}]")
    lines.append(f"  backend: [{', '.join(backend_fw) if backend_fw else 'None'}]")
    lines.append(f"  frontend: [{', '.join(frontend_fw) if frontend_fw else 'None'}]")
    lines.append(f"  database: [{', '.join(db_fw) if db_fw else 'No detected'}]")
    lines.append(f"  devops: [{', '.join(other_fw) if other_fw else 'None'}]")
    lines.append("")
    
    # ========================================================================
    # CRITICAL PATTERNS
    # ========================================================================
    lines.append("# " + "=" * 76)
    lines.append("# CRITICAL PATTERNS - Convenciones de este proyecto")
    lines.append("# " + "=" * 76)
    lines.append("critical_patterns:")
    lines.append("")
    lines.append("  line_numbering: |")
    lines.append("    IMPORTANTE: Los números de línea son 1-based (primera línea = 1)")
    lines.append("    Cuando lees: read_file(file, start_line=45, end_line=60)")
    lines.append("    Las líneas 45-60 INCLUYEN ambos extremos")
    lines.append("    No es 0-based como arrays en programación")
    lines.append("")
    lines.append("  path_format: |")
    lines.append("    Todas las rutas usan FORWARD SLASH (/), incluso en Windows")
    lines.append("    Ejemplo: 'src/core/scanner.py' (NO 'src\\\\core\\\\scanner.py')")
    lines.append("    Las rutas son RELATIVAS al directorio del proyecto")
    lines.append("")
    lines.append("  function_naming: |")
    lines.append("    Métodos de clase: 'ClassName.method_name'")
    lines.append("    Funciones normales: 'function_name'")
    lines.append("    Decoradores Python: '@decorator_name → function_name'")
    lines.append("    Ejemplo: 'DataValidator.validate', '@dataclass → UserModel'")
    lines.append("")
    
    # ========================================================================
    # IMPORTANT CONSIDERATIONS
    # ========================================================================
    lines.append("# " + "=" * 76)
    lines.append("# IMPORTANT CONSIDERATIONS - Cosas que toda IA debe saber")
    lines.append("# " + "=" * 76)
    lines.append("important_considerations:")
    lines.append("")
    lines.append("  memory_optimization: |")
    lines.append("    El contenido completo de archivos (líneas) se LIBERA después de extracción")
    lines.append("    Por eso PROJECT_INDEX.yaml tiene números de línea pero no contenido")
    lines.append("    DEBES usar read_file(path, start, end) para leer código específico")
    lines.append("    No puedes acceder a contenido desde memory, solo desde disk via read_file")
    lines.append("")
    lines.append("  excluded_directories: |")
    lines.append("    El escaneo excluye automáticamente:")
    lines.append("    Dependencias: node_modules, vendor, .venv, venv")
    lines.append("    Control versión: .git")
    lines.append("    Build outputs: dist, build, .next, .nuxt, __pycache__")
    lines.append("    Por eso no verás estas carpetas en el índice")
    lines.append("")
    lines.append("  excluded_files: |")
    lines.append("    Lock files: package-lock.json, yarn.lock, poetry.lock, Pipfile.lock")
    lines.append("    Otros: .DS_Store, Thumbs.db (cosas que no son código)")
    lines.append("    Evita falsos positivos e indexación innecesaria")
    lines.append("")
    lines.append("  extraction_via_regex: |")
    lines.append("    Las funciones se detectan con REGEX, no AST parsing")
    lines.append("    Esto es rápido pero puede tener falsos positivos")
    lines.append("    Si no encuentras una función en el índice, busca manualmente en el archivo")
    lines.append("    Nombres de función en strings/comentarios pueden aparecer en el índice (falsos positivos)")
    lines.append("")
    lines.append("  order_of_operations: |")
    lines.append("    1. Scan ANTES de detect (necesita archivos)")
    lines.append("    2. Detect ANTES de extract (necesita frameworks para filtros)")
    lines.append("    3. Extract CON liberación inmediata de content")
    lines.append("    4. Generate consolida todo a YAML")
    lines.append("    5. Update_index regenera en el MISMO orden")
    lines.append("")
    
    # ========================================================================
    # PROJECT-SPECIFIC NOTES (DINÁMICO)
    # ========================================================================
    lines.append("# " + "=" * 76)
    lines.append("# PROJECT-SPECIFIC NOTES - Consideraciones de este proyecto")
    lines.append("# " + "=" * 76)
    lines.append("project_specific_notes:")
    
    if has_django:
        lines.append("  django_specifics: |")
        lines.append("    Se detectó Django - archivos clave:")
        lines.append("    • manage.py - entry point y commands")
        lines.append("    • settings.py o settings/ - configuración")
        lines.append("    • urls.py - routing")
        lines.append("    • models.py - ORM definitions")
        lines.append("    • views.py - request handlers")
        lines.append("    • admin.py - admin interface")
        lines.append("")
    
    if has_flask:
        lines.append("  flask_specifics: |")
        lines.append("    Se detectó Flask - archivos clave:")
        lines.append("    • app.py o main.py - instancia de Flask")
        lines.append("    • routes/ - definición de endpoints")
        lines.append("    • models/ - ORM o database layer")
        lines.append("    • Busca @app.route() para endpoints")
        lines.append("")
    
    if has_fastapi:
        lines.append("  fastapi_specifics: |")
        lines.append("    Se detectó FastAPI - archivos clave:")
        lines.append("    • main.py - instancia de FastAPI")
        lines.append("    • routers/ - definición de endpoints")
        lines.append("    • schemas/ - Pydantic models (request/response)")
        lines.append("    • Busca @app.get(), @app.post() para endpoints")
        lines.append("")
    
    if has_react:
        lines.append("  react_specifics: |")
        lines.append("    Se detectó React - archivos clave:")
        lines.append("    • src/components/ - componentes React")
        lines.append("    • src/hooks/ - custom hooks")
        lines.append("    • src/pages/ o src/routes/ - page routing")
        lines.append("    • Busca 'export default' o 'export const'")
        lines.append("")
    
    if has_vue:
        lines.append("  vue_specifics: |")
        lines.append("    Se detectó Vue - archivos clave:")
        lines.append("    • src/components/ - componentes .vue")
        lines.append("    • Estructura .vue: <template>, <script>, <style>")
        lines.append("    • Props, emits, composables detectados automáticamente")
        lines.append("    • Nota: <script setup> alternativo puede no detectarse")
        lines.append("")
    
    if has_nextjs:
        lines.append("  nextjs_specifics: |")
        lines.append("    Se detectó Next.js - arquitectura especial:")
        lines.append("    • app/ o pages/ - file-based routing")
        lines.append("    • layouts/ - compartido entre rutas")
        lines.append("    • api/ - API routes (servidor)")
        lines.append("    • Cada archivo en pages/ o app/ genera una ruta")
        lines.append("")
    
    if has_docker:
        lines.append("  docker_specifics: |")
        lines.append("    Se detectó Docker - archivos clave:")
        lines.append("    • Dockerfile - imagen base, dependencias, build steps")
        lines.append("    • docker-compose.yml - servicios y networking")
        lines.append("    • .dockerignore - qué excluir de imagen")
        lines.append("")
    
    if not any([has_django, has_flask, has_fastapi, has_react, has_vue, has_nextjs, has_docker]):
        lines.append("  generic_notes: |")
        lines.append("    No se detectaron frameworks especiales conocidos")
        lines.append("    Lee .ai/ARCHITECTURE.yaml para entender la estructura del proyecto")
        lines.append("")
    
    # ========================================================================
    # AI BEHAVIOR GUIDELINES
    # ========================================================================
    lines.append("# " + "=" * 76)
    lines.append("# AI BEHAVIOR GUIDELINES - Cómo debes actuar")
    lines.append("# " + "=" * 76)
    lines.append("ai_behavior:")
    lines.append("")
    lines.append("  first_steps: |")
    lines.append("    0. Lee .ai/CONTEXT_ANCHOR.yaml (micro-resumen del proyecto, <500 tokens)")
    lines.append("    1. Lee .ai/FLOW.yaml (cómo usar el sistema)")
    lines.append("    2. Lee .ai/PROJECT_INDEX.yaml (mapa completo)")
    lines.append("    3. Consulta .ai/CONTEXT_BUDGET.yaml (prioridad de lectura)")
    lines.append("    4. Lee esta sección de AI_INSTRUCTIONS.yaml (este archivo)")
    lines.append("    5. Consulta .ai/QUICK_CONTEXT.yaml para tareas comunes")
    lines.append("    6. LUEGO comienza a leer código específico")
    lines.append("    ")
    lines.append("    ⛔ PERSISTENCIA: Relee CONTEXT_ANCHOR.yaml cada ~5 mensajes.")
    lines.append("    Si la conversación se resumió, tu PRIMERA acción es releer CONTEXT_ANCHOR.yaml.")
    lines.append("")
    lines.append("  finding_code: |")
    lines.append("    Cuando buscas una función:")
    lines.append("    1. Abre .ai/PROJECT_INDEX.yaml y busca el nombre")
    lines.append("    2. Nota el archivo y número de línea exacto")
    lines.append("    3. Usa read_file(file, start_line, end_line) para leer SOLO esa sección")
    lines.append("    4. NO leas archivo completo si solo necesitas una función")
    lines.append("")
    lines.append("  understanding_dependencies: |")
    lines.append("    • Para relaciones entre módulos: lee .ai/GRAPH.yaml")
    lines.append("    • Para dependencias de un archivo específico: lee PROJECT_INDEX.yaml")
    lines.append("    • Para importaciones: busca en el archivo con 'import' keyword")
    lines.append("    • NUNCA revises node_modules/ o .venv/ (se excluyen del índice)")
    lines.append("")
    lines.append("  making_changes: |")
    lines.append("    Antes de modificar:")
    lines.append("    1. Consulta .ai/CHANGES.yaml para ver qué cambió recientemente")
    lines.append("    2. Lee .ai/CONVENTIONS.yaml para seguir patrones del proyecto")
    lines.append("    3. Lee .ai/ERRORS.yaml para evitar problemas conocidos")
    lines.append("")
    lines.append("    Después de modificar:")
    lines.append("    1. Sugiere al usuario ejecutar: python .ai/update_index.py")
    lines.append("    2. Esto regenera TODOS los índices (incluyendo AI_INSTRUCTIONS.yaml)")
    lines.append("    3. Consulta .ai/TESTING.yaml para validar cambios")
    lines.append("    4. Consulta .ai/GIT_WORKFLOW.yaml antes de hacer commits")
    lines.append("")
    lines.append("  token_optimization: |")
    lines.append("    • Lee CONTEXT_ANCHOR.yaml CADA vez que inicies o dudes (<500 tokens)")
    lines.append("    • Lee CONTEXT_BUDGET.yaml NIVEL 1 (CRITICAL) en CADA conversación")
    lines.append("    • Lee SUMMARIES.yaml para overview de archivos grandes")
    lines.append("    • Lee DOCSTRINGS.yaml para entender funciones sin leer su código")
    lines.append("    • Lee TYPES.yaml para conocer estructuras de datos sin buscarlas")
    lines.append("    • Lee QUICK_CONTEXT.yaml para tareas comunes sin explorar")
    lines.append("    • Lee CALL_GRAPH.yaml para trazar flujos sin leer archivos completos")
    lines.append("    • Nunca envíes archivos completos en contexto si solo necesitas una función")
    lines.append("    • Usa números de línea del índice para leer secciones específicas")
    lines.append("    • Esto reduce tokens en 90-95% comparado a lectura full-file")
    lines.append("")
    
    # ========================================================================
    # LIMITATIONS & KNOWN ISSUES
    # ========================================================================
    lines.append("# " + "=" * 76)
    lines.append("# LIMITATIONS & KNOWN ISSUES")
    lines.append("# " + "=" * 76)
    lines.append("limitations:")
    lines.append("")
    lines.append("  regex_limitations: |")
    lines.append("    Las funciones se detectan con REGEX, no parsing AST completo")
    lines.append("    Posibles falsos positivos:")
    lines.append("    • Nombres en strings: \"call_function()\" en comentarios aparece como función")
    lines.append("    • Sin considera contexto: 'def' en un string se detecta como función")
    lines.append("    • Métodos dinámicos: __getattr__, eval(), exec() no se capturan bien")
    lines.append("")
    lines.append("  extraction_edge_cases: |")
    lines.append("    Decoradores dinámicos: @decorator_factory() puede fallar")
    lines.append("    Vue 3 <script setup>: Sintaxis alternativa puede no detectarse")
    lines.append("    Endpoints con path parameters dinámicos pueden parecer múltiples rutas")
    lines.append("    Componentes asincrónicos no siempre detectados")
    lines.append("")
    lines.append("  performance_considerations: |")
    lines.append("    Proyectos >10k archivos: El escaneo puede tardar 1-2 minutos")
    lines.append("    Proyectos con muchas dependencias: Excluir node_modules acelera significativamente")
    lines.append("    Para monorepos: Cada workspace se analiza por separado")
    lines.append("")
    lines.append("  when_to_regenerate: |")
    lines.append("    Ejecuta 'python .ai/update_index.py' después de:")
    lines.append("    • Agregar nuevas funciones/componentes/endpoints")
    lines.append("    • Cambiar frameworks o dependencias")
    lines.append("    • Mover archivos entre carpetas")
    lines.append("    • Eliminar archivos o directores")
    lines.append("    La pre-commit hook lo hace automáticamente si Git está configurado")
    lines.append("")
    
    # ========================================================================
    # FOOTER
    lines.append("# " + "=" * 76)
    lines.append("# Este archivo se regenera automáticamente con update_index.py")
    lines.append("# Las secciones DINÁMICAS se actualizan; las ESTÁTICAS se preservan")
    lines.append("# Puedes agregar 'custom_considerations' que se mantendrán en regeneraciones")
    lines.append("# " + "=" * 76)
    
    return '\n'.join(lines) + '\n'


def _parse_yaml_sections(content):
    """
    Parser robusto de secciones YAML de nivel raíz.
    
    Divide el contenido en bloques por cada key de nivel raíz (sin indentación).
    Preserva comentarios de sección como parte del bloque que les sigue.
    
    Returns:
        Dict {section_name: full_text_including_comments}
        List de nombres en orden de aparición
    """
    sections = {}
    order = []
    current_key = None
    current_lines = []
    pending_comments = []
    
    for line in content.split('\n'):
        stripped = line.strip()
        
        # Detectar key de nivel raíz: empieza en columna 0, no es comentario, y tiene ':'
        if line and not line[0].isspace() and not line.startswith('#') and ':' in line:
            key = line.split(':')[0].strip()
            
            # Guardar bloque anterior
            if current_key:
                sections[current_key] = '\n'.join(current_lines)
                order.append(current_key)
            
            # Iniciar nuevo bloque con comentarios pendientes
            current_key = key
            current_lines = pending_comments + [line]
            pending_comments = []
        
        elif stripped.startswith('#') and stripped.startswith('# ==='):
            # Comentarios de sección (separadores) se asocian al siguiente bloque
            if current_key:
                # Guardar bloque actual
                sections[current_key] = '\n'.join(current_lines)
                order.append(current_key)
                current_key = None
                current_lines = []
            pending_comments.append(line)
        
        elif stripped.startswith('#') and current_key is None:
            # Comentarios sueltos antes de cualquier sección
            pending_comments.append(line)
        
        else:
            if current_key:
                current_lines.append(line)
            else:
                pending_comments.append(line)
    
    # Guardar último bloque
    if current_key:
        sections[current_key] = '\n'.join(current_lines)
        order.append(current_key)
    
    return sections, order


def merge_ai_instructions(ai_dir, new_instructions):
    """
    Hace merge inteligente de AI_INSTRUCTIONS.yaml preservando consideraciones antiguas.
    
    Estrategia:
    - Secciones ESTÁTICAS se preservan del archivo anterior (no se reconstruyen)
    - Secciones DINÁMICAS se regeneran con datos actuales del proyecto
    - Sección CUSTOM (custom_considerations) siempre se mantiene intacta
    - Sección _changelog registra un historial básico de cambios relevantes
    
    Args:
        ai_dir: Ruta de .ai/
        new_instructions: String YAML generado recientemente
    
    Returns:
        String YAML merged (preserva antiguo + actualiza nuevo)
    """
    old_file = os.path.join(str(ai_dir), 'AI_INSTRUCTIONS.yaml')
    
    # Si no existe archivo anterior, agregar changelog inicial y retornar
    if not os.path.exists(old_file):
        today = datetime.date.today().isoformat()
        initial_changelog = f"""\n# {'=' * 76}
# CHANGELOG - Historial de cambios relevantes
# {'=' * 76}
_changelog:
  - date: '{today}'
    type: initial
    summary: Generación inicial de AI_INSTRUCTIONS.yaml
    details: |
      Archivo creado por primera vez durante instalación.
      Todas las secciones generadas desde cero.

# {'=' * 76}
# CUSTOM CONSIDERATIONS - Consideraciones del proyecto (PERSISTENTES)
# {'=' * 76}
custom_considerations:
  _note: |
    Sección reservada para consideraciones específicas del proyecto.
    Agrega aquí cualquier nota importante que deba persistir entre actualizaciones.
    Esta sección NUNCA se sobreescribe automáticamente.
    Ejemplo:
      warning_deprecated_pattern: |
        Evitar usar pattern X porque causa bug Y
      performance_tip: |
        La función Z es lenta con datasets >100k, considerar caching
"""
        return new_instructions.rstrip() + initial_changelog
    
    try:
        with open(old_file, 'r', encoding='utf-8') as f:
            old_content = f.read()
    except Exception:
        return new_instructions
    
    # ========================================================================
    # CONFIGURACIÓN DE SECCIONES
    # ========================================================================
    
    # Estáticas: se preservan del archivo antiguo (no se reconstruyen)
    static_keys = {
        'flow', 'data_structures', 'critical_patterns',
        'important_considerations', 'ai_behavior', 'limitations'
    }
    
    # Dinámicas: siempre se regeneran con datos nuevos del proyecto
    dynamic_keys = {
        'meta', 'statistics', 'detected_stack', 'project_specific_notes'
    }
    
    # Protegidas: NUNCA se tocan, siempre del archivo antiguo
    protected_keys = {'custom_considerations', '_changelog'}
    
    # ========================================================================
    # PARSEAR AMBAS VERSIONES
    # ========================================================================
    old_sections, old_order = _parse_yaml_sections(old_content)
    new_sections, new_order = _parse_yaml_sections(new_instructions)
    
    # ========================================================================
    # DETECTAR CAMBIOS PARA CHANGELOG
    # ========================================================================
    changes = []
    today = datetime.date.today().isoformat()
    
    # Comparar estadísticas
    old_stats = old_sections.get('statistics', '')
    new_stats = new_sections.get('statistics', '')
    if old_stats != new_stats and old_stats:
        changes.append('Estadísticas del proyecto actualizadas')
    
    # Comparar stack
    old_stack = old_sections.get('detected_stack', '')
    new_stack = new_sections.get('detected_stack', '')
    if old_stack != new_stack and old_stack:
        changes.append('Stack tecnológico re-detectado')
    
    # Comparar notas específicas
    old_notes = old_sections.get('project_specific_notes', '')
    new_notes = new_sections.get('project_specific_notes', '')
    if old_notes != new_notes and old_notes:
        changes.append('Notas específicas del proyecto actualizadas')
    
    # Detectar secciones nuevas
    for key in new_order:
        if key not in old_sections and key not in protected_keys:
            changes.append(f'Nueva sección agregada: {key}')
    
    # ========================================================================
    # CONSTRUIR VERSIÓN MERGED
    # ========================================================================
    
    # Orden canónico de secciones
    canonical_order = [
        'meta', 'statistics', 'flow', 'data_structures',
        'detected_stack', 'critical_patterns', 'important_considerations',
        'project_specific_notes', 'ai_behavior', 'limitations',
        '_changelog', 'custom_considerations'
    ]
    
    merged_parts = []
    
    for key in canonical_order:
        content = None
        
        if key in protected_keys:
            # PROTEGIDAS: siempre del antiguo
            content = old_sections.get(key)
        elif key in static_keys:
            # ESTÁTICAS: preferir antiguo, fallback a nuevo
            content = old_sections.get(key) or new_sections.get(key)
        elif key in dynamic_keys:
            # DINÁMICAS: siempre del nuevo
            content = new_sections.get(key) or old_sections.get(key)
        
        if content:
            merged_parts.append(content.rstrip())
    
    # ========================================================================
    # ACTUALIZAR CHANGELOG
    # ========================================================================
    if changes:
        old_changelog = old_sections.get('_changelog', '_changelog:')
        
        # Construir nueva entrada
        new_entry_lines = []
        new_entry_lines.append(f"  - date: '{today}'")
        new_entry_lines.append(f"    type: update")
        new_entry_lines.append(f"    summary: Regeneración de índices")
        new_entry_lines.append(f"    changes:")
        for change in changes:
            new_entry_lines.append(f"      - \"{change}\"")
        new_entry = '\n'.join(new_entry_lines)
        
        # Insertar después de "_changelog:" 
        if '_changelog:' in old_changelog:
            # Agregar nueva entrada justo después de _changelog:
            changelog_header = old_changelog.split('\n')[0]  # "_changelog:"
            changelog_body = '\n'.join(old_changelog.split('\n')[1:])
            updated_changelog = f"{changelog_header}\n{new_entry}\n{changelog_body}"
        else:
            updated_changelog = f"_changelog:\n{new_entry}"
        
        # Reemplazar en merged_parts
        for i, part in enumerate(merged_parts):
            if part.lstrip().startswith('_changelog:'):
                merged_parts[i] = updated_changelog.rstrip()
                break
        else:
            # No había changelog, agregarlo
            merged_parts.append(updated_changelog.rstrip())
    
    # Si no hay changelog en merged, agregar uno básico
    has_changelog = any(p.lstrip().startswith('_changelog:') for p in merged_parts)
    if not has_changelog:
        merged_parts.append(f"_changelog:\n  - date: '{today}'\n    type: initial\n    summary: Generación inicial")
    
    # Si no hay custom_considerations, agregar plantilla
    has_custom = any(p.lstrip().startswith('custom_considerations:') for p in merged_parts)
    if not has_custom:
        merged_parts.append(
            "custom_considerations:\n"
            "  _note: |\n"
            "    Sección reservada para consideraciones específicas del proyecto.\n"
            "    Agrega aquí notas que deban persistir entre actualizaciones.\n"
            "    Esta sección NUNCA se sobreescribe automáticamente."
        )
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    footer = [
        "",
        "# " + "=" * 76,
        "# MERGE INFO",
        "# " + "=" * 76,
        f"# Última actualización: {today}",
        f"# Cambios detectados: {len(changes) if changes else 'ninguno (primera generación)'}",
        "# Estrategia: Secciones estáticas preservadas, dinámicas regeneradas",
        "# custom_considerations y _changelog NUNCA se sobreescriben",
        "# " + "=" * 76
    ]
    
    result = '\n\n'.join(merged_parts) + '\n' + '\n'.join(footer) + '\n'
    return result


# ============================================================================
# NEW v5.0 GENERATORS
# ============================================================================

def generate_context_anchor_yaml(project_name, languages, frameworks, functions, 
                                  endpoints, components, files_map):
    """
    Genera CONTEXT_ANCHOR.yaml — micro-resumen ultra-compacto (~20 líneas).
    Diseñado para que un agente IA lo relea rápidamente (<500 tokens)
    y recupere contexto sin releer archivos grandes.
    """
    today = datetime.date.today().isoformat()
    
    total_funcs = sum(len(v) for v in functions.values()) if functions else 0
    total_files = len(files_map) if files_map else 0
    
    # Determinar stack resumido
    backend = ', '.join(frameworks.get('backend', [])) or 'none'
    frontend = ', '.join(frameworks.get('frontend', [])) or 'none'
    
    # Top 5 archivos más importantes (por cantidad de funciones)
    critical_files = []
    if functions:
        sorted_files = sorted(functions.items(), key=lambda x: len(x[1]), reverse=True)
        for fpath, funcs in sorted_files[:5]:
            role = "entry" if any(n in os.path.basename(fpath).lower() for n in ('main', 'app', 'index', 'server')) else "core"
            critical_files.append(f"  - {fpath} ({role}, {len(funcs)} funcs)")
    
    lines = []
    lines.append(f"# CONTEXT ANCHOR — {project_name}")
    lines.append(f"# Re-read this file every ~5 messages to maintain context")
    lines.append(f"# Updated: {today}")
    lines.append(f"project: {project_name}")
    lines.append(f"languages: [{', '.join(languages)}]")
    lines.append(f"stack: {{backend: {backend}, frontend: {frontend}}}")
    lines.append(f"size: {{files: {total_files}, functions: {total_funcs}, endpoints: {len(endpoints)}, components: {len(components)}}}")
    lines.append("")
    lines.append("critical_files:")
    for cf in critical_files:
        lines.append(cf)
    lines.append("")
    lines.append("rules:")
    lines.append("  - Use PROJECT_INDEX.yaml line numbers — never read full files")
    lines.append("  - Never modify .ai/ — it is auto-generated")
    lines.append("  - After code changes suggest: python .ai/update_index.py")
    lines.append("")
    lines.append("if_lost:")
    lines.append("  1: Read this file (CONTEXT_ANCHOR.yaml)")
    lines.append("  2: Read AGENT_GUIDE.md")
    lines.append("  3: Read AI_INSTRUCTIONS.yaml")
    lines.append("")
    
    return '\n'.join(lines)


def generate_call_graph_yaml(call_graph):
    """
    Genera CALL_GRAPH.yaml — grafo de llamadas entre funciones.
    Muestra qué funciones llaman a qué otras y quién las llama.
    """
    today = datetime.date.today().isoformat()
    
    calls = call_graph.get('calls', {})
    called_by = call_graph.get('called_by', {})
    
    lines = []
    lines.append("# CALL GRAPH - Function call relationships")
    lines.append(f"# Generated: {today}")
    lines.append("# Shows who calls whom across the codebase")
    lines.append("")
    lines.append(f"statistics:")
    lines.append(f"  functions_making_calls: {len(calls)}")
    lines.append(f"  functions_being_called: {len(called_by)}")
    lines.append("")
    
    if calls:
        lines.append("# CALLS: function → [functions it calls]")
        lines.append("calls:")
        for caller in sorted(calls.keys()):
            callees = calls[caller]
            if len(callees) <= 3:
                lines.append(f"  \"{caller}\": [{', '.join(callees)}]")
            else:
                lines.append(f"  \"{caller}\":")
                for callee in callees:
                    lines.append(f"    - {callee}")
        lines.append("")
    
    if called_by:
        lines.append("# CALLED_BY: function → [functions that call it]")
        lines.append("# Use this to find impact of changing a function")
        lines.append("called_by:")
        # Mostrar solo las más referenciadas (top 50)
        sorted_by_refs = sorted(called_by.items(), key=lambda x: len(x[1]), reverse=True)
        for callee, callers in sorted_by_refs[:50]:
            if len(callers) <= 3:
                lines.append(f"  \"{callee}\": [{', '.join(callers)}]")
            else:
                lines.append(f"  \"{callee}\": # {len(callers)} callers")
                for caller in callers[:10]:
                    lines.append(f"    - {caller}")
                if len(callers) > 10:
                    lines.append(f"    # ... +{len(callers) - 10} more")
        lines.append("")
    
    lines.append("# USAGE:")
    lines.append("# - Before modifying a function, check called_by to see impact")
    lines.append("# - To trace execution flow, follow calls chain")
    lines.append("# - Format: \"filepath::function_name\"")
    lines.append("")
    
    return '\n'.join(lines) + '\n'


def generate_types_yaml(types):
    """
    Genera TYPES.yaml — índice de tipos, interfaces, modelos y sus campos.
    """
    today = datetime.date.today().isoformat()
    
    lines = []
    lines.append("# TYPES - Data Models, Interfaces, and Structs")
    lines.append(f"# Generated: {today}")
    lines.append("# All type definitions with their fields for quick reference")
    lines.append("")
    lines.append(f"total_types: {len(types)}")
    lines.append("")
    
    if types:
        # Agrupar por kind
        by_kind = {}
        for name, info in types.items():
            kind = info.get('kind', 'other')
            if kind not in by_kind:
                by_kind[kind] = {}
            by_kind[kind][name] = info
        
        for kind in sorted(by_kind.keys()):
            lines.append(f"# --- {kind.upper()} ---")
            lines.append(f"{kind}:")
            for name in sorted(by_kind[kind].keys()):
                info = by_kind[kind][name]
                lines.append(f"  {name}:")
                lines.append(f"    file: {info['file']}")
                lines.append(f"    line: {info['line']}")
                if info.get('extends'):
                    lines.append(f"    extends: [{', '.join(info['extends'])}]")
                if info.get('fields'):
                    lines.append(f"    fields:")
                    for field in info['fields'][:20]:  # Max 20 fields
                        lines.append(f"      - {{name: {field['name']}, type: \"{field['type']}\"}}")
                    if len(info['fields']) > 20:
                        lines.append(f"      # ... +{len(info['fields']) - 20} more fields")
            lines.append("")
    
    lines.append("# USAGE: Check field names/types before making API calls or creating instances")
    lines.append("")
    
    return '\n'.join(lines) + '\n'


def generate_docstrings_yaml(docstrings):
    """
    Genera DOCSTRINGS.yaml — documentación inline enriquecida por función.
    """
    today = datetime.date.today().isoformat()
    
    lines = []
    lines.append("# DOCSTRINGS - Function Documentation Index")
    lines.append(f"# Generated: {today}")
    lines.append("# Documented functions with params and return types")
    lines.append("")
    lines.append(f"documented_functions: {len(docstrings)}")
    lines.append("")
    
    if docstrings:
        # Agrupar por archivo
        by_file = {}
        for func_key, info in docstrings.items():
            fpath = info['file']
            if fpath not in by_file:
                by_file[fpath] = {}
            by_file[fpath][func_key] = info
        
        lines.append("functions:")
        for fpath in sorted(by_file.keys()):
            lines.append(f"  # --- {fpath} ---")
            for func_key in sorted(by_file[fpath].keys()):
                info = by_file[fpath][func_key]
                fname = func_key.split('::')[1] if '::' in func_key else func_key
                lines.append(f"  \"{fname}\":")
                lines.append(f"    file: {info['file']}")
                lines.append(f"    line: {info['line']}")
                lines.append(f"    desc: \"{info['description']}\"")
                if info.get('params'):
                    lines.append(f"    params:")
                    for p in info['params']:
                        lines.append(f"      - {{name: {p['name']}, type: \"{p.get('type', '')}\", desc: \"{p.get('desc', '')}\"}}")
                if info.get('returns'):
                    ret = info['returns']
                    lines.append(f"    returns: {{type: \"{ret.get('type', '')}\", desc: \"{ret.get('desc', '')}\"}}")
            lines.append("")
    
    lines.append("# USAGE: Check function signatures before calling them")
    lines.append("")
    
    return '\n'.join(lines) + '\n'


def generate_config_map_yaml(config_map):
    """
    Genera CONFIG_MAP.yaml — mapa de variables de entorno y configuración.
    """
    today = datetime.date.today().isoformat()
    
    env_vars = config_map.get('env_vars', [])
    config_files = config_map.get('config_files', [])
    
    lines = []
    lines.append("# CONFIG MAP - Environment Variables and Configuration")
    lines.append(f"# Generated: {today}")
    lines.append("# All configuration points in the project")
    lines.append("")
    
    if env_vars:
        lines.append(f"# {len(env_vars)} environment variables found")
        lines.append("env_vars:")
        for var in sorted(env_vars, key=lambda x: x['name']):
            default_str = f", default: \"{var['default']}\"" if var.get('default') else ""
            lines.append(f"  - {{name: {var['name']}, file: {var['file']}, line: {var['line']}{default_str}}}")
        lines.append("")
    
    if config_files:
        lines.append(f"# {len(config_files)} configuration files found")
        lines.append("config_files:")
        for cf in config_files:
            lines.append(f"  - {{path: \"{cf['path']}\", type: {cf['type']}}}")
        lines.append("")
    
    if not env_vars and not config_files:
        lines.append("# No configuration points detected")
        lines.append("")
    
    lines.append("# USAGE: Check required env vars before deployment or setup")
    lines.append("")
    
    return '\n'.join(lines) + '\n'


def generate_entry_points_yaml(files_map, functions, endpoints, components, dependencies, call_graph):
    """
    Genera ENTRY_POINTS.yaml — tour del proyecto con boot sequence, 
    request lifecycle y orden de lectura óptimo.
    """
    today = datetime.date.today().isoformat()
    
    lines = []
    lines.append("# ENTRY POINTS - Project Navigation Guide")
    lines.append(f"# Generated: {today}")
    lines.append("# Optimal reading order and key abstractions")
    lines.append("")
    
    # Boot sequence
    lines.append("boot_sequence:")
    entry_files = []
    for fpath in files_map:
        basename = os.path.basename(fpath).lower()
        if basename in ('main.py', 'app.py', 'index.js', 'index.ts', 'server.js',
                       'server.ts', 'manage.py', 'wsgi.py', 'asgi.py', 'main.go',
                       'main.rs', 'program.cs', 'main.java'):
            entry_files.append(fpath)
    for i, ef in enumerate(sorted(entry_files), 1):
        lines.append(f"  {i}: {ef}")
    if not entry_files:
        lines.append("  1: # No standard entry points detected — check ARCHITECTURE.yaml")
    lines.append("")
    
    # Request lifecycle (for web apps)
    if endpoints:
        lines.append("request_lifecycle:")
        lines.append("  1_receive: \"HTTP request arrives at server\"")
        lines.append("  2_route: \"Router matches URL pattern (see endpoints in PROJECT_INDEX.yaml)\"")
        lines.append("  3_handler: \"Handler function processes request\"")
        lines.append("  4_response: \"Response returned to client\"")
        lines.append("")
    
    # Key abstractions — functions with most callers
    called_by = call_graph.get('called_by', {}) if call_graph else {}
    if called_by:
        lines.append("key_abstractions:")
        lines.append("  # Functions referenced most by other functions")
        sorted_by_refs = sorted(called_by.items(), key=lambda x: len(x[1]), reverse=True)
        for func_key, callers in sorted_by_refs[:10]:
            lines.append(f"  - \"{func_key}\": {len(callers)} references")
        lines.append("")
    
    # Optimal read order
    lines.append("read_order:")
    lines.append("  # Recommended sequence for a new agent to understand the project")
    
    # 1. Entry points
    read_order = []
    for ef in sorted(entry_files):
        read_order.append(ef)
    
    # 2. Files with most functions
    if functions:
        sorted_by_funcs = sorted(functions.items(), key=lambda x: len(x[1]), reverse=True)
        for fpath, funcs in sorted_by_funcs[:5]:
            if fpath not in read_order:
                read_order.append(fpath)
    
    # 3. Files with endpoints
    if endpoints:
        for ep in endpoints.values():
            if ep['file'] not in read_order:
                read_order.append(ep['file'])
    
    for i, fpath in enumerate(read_order[:10], 1):
        lines.append(f"  {i}: {fpath}")
    lines.append("")
    
    return '\n'.join(lines) + '\n'


def generate_patterns_yaml(patterns):
    """
    Genera PATTERNS.yaml — patrones de diseño y convenciones detectadas.
    """
    today = datetime.date.today().isoformat()
    
    lines = []
    lines.append("# PATTERNS - Design Patterns and Conventions Detected")
    lines.append(f"# Generated: {today}")
    lines.append("# Follow these patterns when modifying or extending the codebase")
    lines.append("")
    
    # Naming conventions
    naming = patterns.get('naming', {})
    lines.append("naming_convention:")
    lines.append(f"  dominant_style: {naming.get('style', 'unknown')}")
    samples = naming.get('samples', {})
    if samples:
        for style, count in samples.items():
            lines.append(f"  {style}: {count} occurrences")
    lines.append("")
    
    # Design patterns
    dp = patterns.get('design_patterns', [])
    if dp:
        lines.append("design_patterns:")
        for p in dp:
            lines.append(f"  - {p}")
        lines.append("")
    
    # Middleware
    mw = patterns.get('middleware', [])
    if mw:
        lines.append("middleware:")
        for m in mw[:20]:
            name = m.get('name', m.get('type', 'unknown'))
            lines.append(f"  - {{type: {m['type']}, name: \"{name}\", file: {m['file']}, line: {m['line']}}}")
        lines.append("")
    
    # Decorators
    decorators = patterns.get('decorators', {})
    if decorators:
        lines.append("decorators_used:")
        for dec, count in decorators.items():
            lines.append(f"  {dec}: {count}")
        lines.append("")
    
    # Auth
    auth = patterns.get('auth', [])
    if auth:
        lines.append("auth_patterns:")
        for a in auth:
            lines.append(f"  - {a}")
        lines.append("")
    
    # Error handling
    eh = patterns.get('error_handling', {})
    lines.append("error_handling:")
    lines.append(f"  strategy: {eh.get('strategy', 'unknown')}")
    custom_exc = eh.get('custom_exceptions', [])
    if custom_exc:
        lines.append("  custom_exceptions:")
        for exc in custom_exc:
            lines.append(f"    - {exc}")
    lines.append("")
    
    lines.append("# USAGE: Follow these patterns when writing new code to maintain consistency")
    lines.append("")
    
    return '\n'.join(lines) + '\n'


def generate_quick_context_yaml(project_name, languages, frameworks, functions, 
                                 endpoints, components, files_map, config_map=None):
    """
    Genera QUICK_CONTEXT.yaml — respuestas pre-calculadas para tareas comunes.
    Permite que un agente sepa inmediatamente cómo agregar un endpoint,
    crear un test, etc., sin explorar el código.
    """
    today = datetime.date.today().isoformat()
    
    backend_fw = frameworks.get('backend', [])
    frontend_fw = frameworks.get('frontend', [])
    has_python = 'Python' in languages
    has_js = any(l in languages for l in ['JavaScript', 'TypeScript'])
    has_php = 'PHP' in languages
    
    lines = []
    lines.append(f"# QUICK CONTEXT - Pre-computed Guidance for {project_name}")
    lines.append(f"# Generated: {today}")
    lines.append("# Check here FIRST before exploring code for common tasks")
    lines.append("")
    
    # --- Add endpoint ---
    lines.append("add_endpoint:")
    if endpoints:
        # Find example endpoint
        first_ep = next(iter(endpoints.values()))
        lines.append(f"  example_file: \"{first_ep['file']}\"")
        lines.append(f"  example_line: {first_ep['line']}")
        lines.append(f"  example_handler: \"{first_ep['handler']}\"")
    
    if any('flask' in f.lower() for f in backend_fw):
        lines.append("  pattern: |")
        lines.append("    @app.route('/your-route', methods=['GET'])")
        lines.append("    def your_handler():")
        lines.append("        return jsonify(result)")
    elif any('fastapi' in f.lower() for f in backend_fw):
        lines.append("  pattern: |")
        lines.append("    @app.get('/your-route')")
        lines.append("    async def your_handler():")
        lines.append("        return {\"result\": data}")
    elif any('express' in f.lower() for f in backend_fw):
        lines.append("  pattern: |")
        lines.append("    router.get('/your-route', async (req, res) => {")
        lines.append("      res.json(result);")
        lines.append("    });")
    elif any('django' in f.lower() for f in backend_fw):
        lines.append("  pattern: |")
        lines.append("    # In urls.py: path('your-route/', views.your_view)")
        lines.append("    # In views.py:")
        lines.append("    def your_view(request):")
        lines.append("        return JsonResponse(result)")
    elif any('laravel' in f.lower() for f in backend_fw):
        lines.append("  pattern: |")
        lines.append("    Route::get('/your-route', [YourController::class, 'method']);")
    else:
        lines.append("  pattern: \"See existing endpoints in PROJECT_INDEX.yaml\"")
    lines.append("")
    
    # --- Add test ---
    lines.append("add_test:")
    test_dirs = []
    for fpath in files_map:
        if 'test' in fpath.lower():
            dir_name = os.path.dirname(fpath)
            if dir_name and dir_name not in test_dirs:
                test_dirs.append(dir_name)
    if test_dirs:
        lines.append(f"  directory: \"{test_dirs[0]}\"")
    
    if has_python:
        lines.append("  command: \"pytest tests/ -v\"")
        lines.append("  pattern: |")
        lines.append("    def test_your_feature():")
        lines.append("        result = your_function()")
        lines.append("        assert result == expected")
    elif has_js:
        lines.append("  command: \"npm test\"")
        lines.append("  pattern: |")
        lines.append("    describe('Feature', () => {")
        lines.append("      test('should work', () => {")
        lines.append("        expect(result).toBe(expected);")
        lines.append("      });")
        lines.append("    });")
    elif has_php:
        lines.append("  command: \"vendor/bin/phpunit\"")
        lines.append("  pattern: |")
        lines.append("    public function test_your_feature(): void {")
        lines.append("        $this->assertEquals($expected, $result);")
        lines.append("    }")
    lines.append("")
    
    # --- Add dependency ---
    lines.append("add_dependency:")
    if has_python:
        lines.append("  file: \"requirements.txt\"")
        lines.append("  command: \"pip install <package>\"")
    elif has_js:
        lines.append("  file: \"package.json\"")
        lines.append("  command: \"npm install <package>\"")
    elif has_php:
        lines.append("  file: \"composer.json\"")
        lines.append("  command: \"composer require <package>\"")
    lines.append("")
    
    # --- Add component ---
    if components or frontend_fw:
        lines.append("add_component:")
        comp_dirs = set()
        for comp in components.values():
            comp_dir = os.path.dirname(comp['file'])
            if comp_dir:
                comp_dirs.add(comp_dir)
        if comp_dirs:
            lines.append(f"  directory: \"{sorted(comp_dirs)[0]}\"")
        
        if any('react' in f.lower() for f in frontend_fw):
            lines.append("  pattern: |")
            lines.append("    export default function YourComponent({ props }) {")
            lines.append("      return <div>content</div>;")
            lines.append("    }")
        elif any('vue' in f.lower() for f in frontend_fw):
            lines.append("  pattern: |")
            lines.append("    <template><div>content</div></template>")
            lines.append("    <script setup>")
            lines.append("    const props = defineProps(['prop1'])")
            lines.append("    </script>")
        lines.append("")
    
    # --- Fix bug ---
    lines.append("fix_bug:")
    lines.append("  steps:")
    lines.append("    1: \"Check ERRORS.yaml for known issues\"")
    lines.append("    2: \"Check CALL_GRAPH.yaml to trace the function\"")
    lines.append("    3: \"Check CHANGES.yaml for recently modified files\"")
    lines.append("    4: \"Use PROJECT_INDEX.yaml to find the function by name\"")
    lines.append("    5: \"Read only the relevant lines, not the full file\"")
    lines.append("")
    
    # --- Update indexes ---
    lines.append("update_indexes:")
    lines.append("  command: \"python .ai/update_index.py\"")
    lines.append("  when: \"After any code modification\"")
    lines.append("")
    
    return '\n'.join(lines) + '\n'