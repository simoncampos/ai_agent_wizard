"""
Generador consolidado de todos los archivos .ai/
Importa funciones del instalador original para reutilización
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
    lines.append("# PURPOSE: Machine-readable project map for AI assistants.")
    lines.append("# USAGE: Read this file FIRST before any codebase modification task.")
    lines.append("# UPDATE: After ANY code change, update affected sections immediately.")
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

    lines.append("# Para actualizar: python .ai/update_index.py")
    
    return '\n'.join(lines) + '\n'


def generate_all_yamls(project_name, languages, frameworks):
    """Genera todos los YAMLs necesarios de forma consolidada"""
    today = datetime.date.today().isoformat()
    
    has_python = 'Python' in languages
    has_js = any('JavaScript' in l or 'TypeScript' in l for l in languages)
    
    yamls = {}
    
    # CONVENTIONS.yaml
    yamls['CONVENTIONS.yaml'] = f"""# {project_name.upper()} - CONVENTIONS
# LAST_UPDATED: {today}

naming:
  {'files_python: snake_case.py' if has_python else ''}
  {'functions_python: snake_case' if has_python else ''}
  {'files_javascript: camelCase.js' if has_js else ''}
  css_classes: kebab-case

code_style:
  indentation: "4 espacios"
  {'quotes_python: "comillas dobles"' if has_python else ''}
  max_line_length: 120

file_locations:
  new_component: "src/components/"
  new_utility: "src/utils/"
  new_test: "tests/"
"""
    
    # TESTING.yaml
    backend_fw = frameworks.get('backend', [])
    test_cmd = 'pytest tests/ -v' if any('python' in f.lower() for f in backend_fw) else 'npm test'
    
    yamls['TESTING.yaml'] = f"""# {project_name.upper()} - TESTING
# LAST_UPDATED: {today}

health_checks:
  - name: Sistema activo
    cmd: "echo OK"

test_commands:
  unit: "{test_cmd}"

quick_validation:
  python: "python -m py_compile {{archivo}}"
  javascript: "node --check {{archivo}}"
  json: "python -m json.tool {{archivo}} > /dev/null"
"""
    
    # ERRORS.yaml
    yamls['ERRORS.yaml'] = f"""# {project_name.upper()} - ERRORS
# LAST_UPDATED: {today}

common_errors:
  - pattern: "ModuleNotFoundError"
    cause: Dependencia no instalada
    fix: "Instalar con pip/npm"

restart_procedures:
  full: "Reiniciar aplicación"
"""
    
    # GIT_WORKFLOW.yaml
    yamls['GIT_WORKFLOW.yaml'] = f"""# {project_name.upper()} - GIT WORKFLOW
# LAST_UPDATED: {today}

repository:
  main_branch: "main"
  current_version: "v0.1.0"

commit_policy:
  format: "conventional_commits"
  types:
    feat: "Nueva funcionalidad"
    fix: "Corrección de bug"
    docs: "Documentación"
    refactor: "Refactorización"
    test: "Tests"
    chore: "Mantenimiento"

versioning:
  scheme: "semver"
  tag_format: "vMAJOR.MINOR.PATCH"

protected_files:
  never_commit:
    - ".env"
    - "*.key"
    - "*credentials*"
"""
    
    return yamls
