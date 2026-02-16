"""
Generador consolidado de todos los archivos .ai/
Crea índices con acceso directo a funciones, eliminando navegación manual.
Importa funciones del instalador original para reutilización.
"""

import datetime


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


def generate_all_yamls(project_name, languages, frameworks):
    """Genera todos los YAMLs necesarios con mínima información"""
    today = datetime.date.today().isoformat()
    
    has_python = 'Python' in languages
    has_js = any('JavaScript' in l or 'TypeScript' in l for l in languages)
    
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
    
    # TESTING.yaml
    backend_fw = frameworks.get('backend', [])
    test_cmd = 'pytest tests/ -v' if any('python' in f.lower() for f in backend_fw) else 'npm test'
    
    yamls['TESTING.yaml'] = f"""# {project_name} Testing
# Last Updated: {today}

test_commands:
  unit: "{test_cmd}"
"""
    
    # ERRORS.yaml
    yamls['ERRORS.yaml'] = f"""# {project_name} Common Errors
# Last Updated: {today}

common_errors:
  - pattern: "ModuleNotFoundError"
    cause: Missing dependency
    fix: Install with pip/npm
"""
    
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


def generate_architecture_yaml(project_path):
    """Genera ARCHITECTURE.yaml explicando el flujo del proyecto optimizado"""
    return """# PROJECT ARCHITECTURE
# Understand the optimized project structure and execution flow

project_purpose: |
  Reduce token usage in AI interactions by up to 95% through intelligent indexing.
  Replaces manual file navigation with direct code location access (file + line number).

optimizer_purpose: |
  This .ai/ system was created to help AI agents understand your project efficiently.
  It maps code structure so every function, endpoint, and component is immediately accessible.

## EXECUTION FLOW
flow:
  1_scan:
    module: core.scanner
    purpose: Map all project files and their sizes
    functions: [scan_files, iter_source_files]
    output: Files map with paths, types, line counts
    
  2_detect:
    module: core.detectors
    purpose: Identify programming languages and frameworks
    functions: [detect_languages, detect_frameworks, detect_services, detect_monorepo]
    output: Technology stack (Python, JS, Django, React, etc)
    
  3_extract:
    module: core.extractors
    purpose: Find functions, API endpoints, UI components, and dependencies
    functions: [extract_functions, extract_endpoints, extract_vue_components, extract_dependencies]
    output: Code elements with exact line numbers
    
  4_generate:
    module: generators.all_generators
    purpose: Create YAML index files for quick AI reference
    functions: [generate_project_index, generate_all_yamls]
    output: PROJECT_INDEX.yaml + configuration YAMLs
    
  5_install:
    module: main
    purpose: Place .ai/ folder with all indexes in project root
    triggers: All config files, update scripts, and this file

## MODULE DEPENDENCIES
modules:
  core/scanner.py:
    imports: os, pathlib, core.detectors
    provides: File listing, directory traversal
    used_by: [main.install, core.extractors]
    
  core/detectors.py:
    imports: os, json, re
    provides: Language/framework detection
    used_by: [main.install, generators]
    
  core/extractors.py:
    imports: re, yaml
    provides: Code element parsing
    used_by: [main.install, generators]
    
  generators/all_generators.py:
    imports: datetime
    provides: YAML generation functions
    used_by: [main.install, update_index.py, update.py]

## KEY CONCEPTS
concepts:
  PROJECT_INDEX.yaml:
    what: Master index mapping every function/class/endpoint
    why: AI agents read this instead of scanning entire codebase
    benefit: 95% token reduction per interaction
    
  Direct Access:
    what: Line numbers for every code element
    why: Jump directly to code, no searching needed
    benefit: Instant context, eliminates navigation time
    
  Incremental Updates:
    what: update_index.py regenerates without full reinstall
    why: Fast re-indexing after local code changes
    benefit: Development workflow stays fast
    
  Auto-Detection:
    what: System detects project type automatically
    why: Same tool works for Python, JS, mono-repos, etc
    benefit: Universal, zero configuration needed

## UNDERSTANDING YOUR PROJECT
understand_your_project: |
  When .ai/ is installed, it analyzes:
  - Every .py, .js, .ts, .go, .java file
  - Function definitions and their line numbers
  - API routes and endpoints
  - Component structure (React, Vue components)
  - Import relationships and dependencies
  - Technology stack and frameworks
  
  All this data is stored in yaml files under .ai/
  AI agents read these yamls instead of scanning your code.

## REGENERATING INDEXES
regenerate: |
  After you modify code locally:
    python .ai/update_index.py
  
  When you want latest features from GitHub:
    python .ai/update.py --auto
  
  Both automatically regenerate all indexes.
"""


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
    """Genera GRAPH.yaml - mapa comprimido de dependencias y relaciones"""
    total_funcs = sum(len(v) for v in functions.values()) if functions else 0
    total_deps = len(dependencies) if dependencies else 0
    total_eps = len(endpoints) if endpoints else 0
    total_comps = len(components) if components else 0
    
    return f"""# DEPENDENCY GRAPH - Compressed module relationships
# Quick visual reference for understanding code flow

module_relationships: |
  This is a compressed view of how modules depend on each other.
  Read this FIRST when you need to understand the flow.

core_modules:
  scanner: [detectors]
  detectors: []
  extractors: [detectors, scanner]
  generators: [extractors]
  main: [scanner, detectors, extractors, generators]

data_flow: |
  FILES → scanner.scan_files()
    ↓
  LANGUAGES → detectors.detect_languages()
    ↓  
  FRAMEWORKS → detectors.detect_frameworks()
    ↓
  FUNCTIONS → extractors.extract_functions()
  ENDPOINTS → extractors.extract_endpoints()
  COMPONENTS → extractors.extract_vue_components()
  DEPENDENCIES → extractors.extract_dependencies()
    ↓
  INDEXES → generators.generate_project_index()
    ↓
  .ai/ FILES → Installation complete

key_entry_points:
  main.install: "Orchestrates all 5 phases"
  phase_1: "Validation"
  phase_2: "Detection"
  phase_3: "Extraction"
  phase_4: "Generation"
  phase_5: "Installation"

critical_paths:
  search: "Project Index → Function name → Line number"
  trace: "Dependencies → File relations → Function calls"
  find_endpoint: "Endpoints → Handler → File line"

statistics:
  total_functions: {total_funcs}
  total_endpoints: {total_eps}
  total_components: {total_comps}
  total_dependencies: {total_deps}
"""