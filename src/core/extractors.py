"""
Extractores de información del código fuente.
Extrae funciones, endpoints API, componentes UI y dependencias con números
de línea exactos para eliminar navegación manual entre archivos.
"""

import re
import os

try:
    from utils.warnings import warn, vprint
except ImportError:
    def warn(msg, ctx=""): pass
    def vprint(msg, level=1): pass


def extract_functions(files_map):
    """
    Extrae funciones/clases con numeros de linea exactos.
    
    Soporta:
    - Python: def, async def, class
    - JavaScript/TypeScript: function, arrow functions, class, const func =
    - Go: func, type struct
    - Rust: fn, struct, enum
    - Java: metodos publicos/privados, class
    - Ruby: def, class
    - PHP: function, class
    
    Args:
        files_map: Dict {filepath: {'type': 'py', 'lines': N, 'content': [lines]}}
    
    Returns:
        Dict {filepath: {function_name: line_number}}
        
    Notas:
        - Para Python detecta metodos de clase como "ClassName.method_name"
        - Ignora funciones dentro de condicionales inline
        - Los numeros de linea son 1-based (primera linea = 1)
    
    Limitaciones:
        - No detecta funciones lambda/anonimas
        - No maneja decoradores complejos en Python
        - No distingue funciones publicas/privadas en TypeScript
    """
    vprint("Extrayendo funciones...", level=1)
    
    functions = {}

    patterns = {
        'py': [
            (r'^(\s*)def\s+(\w+)\s*\(', 'function'),
            (r'^(\s*)class\s+(\w+)', 'class'),
            (r'^(\s*)async\s+def\s+(\w+)\s*\(', 'async_function'),
        ],
        'js': [
            (r'^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)', 'function'),
            (r'^\s*(?:export\s+)?const\s+(\w+)\s*=\s*(?:async\s*)?\(', 'arrow'),
            (r'^\s*(?:export\s+)?const\s+(\w+)\s*=\s*\{', 'object'),
            (r'^\s*(?:export\s+)?class\s+(\w+)', 'class'),
            (r'^\s*(\w+)\s*\(.*\)\s*\{', 'method'),
        ],
        'ts': None,  # Usa los mismos patrones que JS
        'tsx': None,
        'jsx': None,
        'go': [
            (r'^func\s+(?:\(\w+\s+\*?\w+\)\s+)?(\w+)\s*\(', 'function'),
            (r'^type\s+(\w+)\s+struct', 'struct'),
        ],
        'rs': [
            (r'^\s*(?:pub\s+)?fn\s+(\w+)', 'function'),
            (r'^\s*(?:pub\s+)?struct\s+(\w+)', 'struct'),
            (r'^\s*(?:pub\s+)?enum\s+(\w+)', 'enum'),
        ],
        'java': [
            (r'^\s*(?:public|private|protected)?\s*(?:static\s+)?(?:\w+\s+)+(\w+)\s*\(', 'method'),
            (r'^\s*(?:public\s+)?class\s+(\w+)', 'class'),
        ],
        'rb': [
            (r'^\s*def\s+(\w+)', 'method'),
            (r'^\s*class\s+(\w+)', 'class'),
        ],
        'php': [
            (r'^\s*(?:public|private|protected)?\s*function\s+(\w+)', 'function'),
            (r'^\s*class\s+(\w+)', 'class'),
        ],
    }

    for filepath, info in files_map.items():
        ext = info['type']
        pats = patterns.get(ext)
        if pats is None and ext in ('ts', 'tsx', 'jsx'):
            pats = patterns.get('js')
        if not pats:
            continue

        file_funcs = {}
        current_class = None

        for i, line in enumerate(info['content'], 1):
            for pattern, kind in pats:
                if ext == 'py':
                    m = re.match(pattern, line)
                    if m:
                        indent = len(m.group(1))
                        name = m.group(2)
                        if kind == 'class':
                            current_class = name
                            file_funcs[name] = i
                        elif indent > 0 and current_class:
                            file_funcs[f"{current_class}.{name}"] = i
                        else:
                            current_class = None
                            file_funcs[name] = i
                else:
                    m = re.match(pattern, line)
                    if m:
                        name = m.group(1) if m.lastindex else m.group(0).strip()
                        if name and not name.startswith(('if', 'for', 'while', 'switch', 'return', 'else')):
                            file_funcs[name] = i

        if file_funcs:
            functions[filepath] = file_funcs
            vprint(f"{filepath}: {len(file_funcs)} funciones", level=2)

    vprint(f"Total funciones extraidas: {sum(len(v) for v in functions.values())}", level=1)
    return functions


def extract_endpoints(files_map):
    """
    Extrae endpoints API de frameworks web.
    
    Soporta:
    - Flask: @app.route / @blueprint.route
    - FastAPI: @app.get / @router.get / etc.
    - Express: app.get / router.post / etc.
    
    Args:
        files_map: Dict con contenido de archivos
        
    Returns:
        Dict {endpoint_key: {'handler': str, 'file': str, 'line': int}}
    """
    vprint("Extrayendo endpoints API...", level=1)
    
    endpoints = {}

    flask_pattern = re.compile(
        r"""@\w+\.route\(\s*['"]([^'"]+)['"]\s*(?:,\s*methods\s*=\s*\[([^\]]+)\])?\s*\)"""
    )
    express_pattern = re.compile(
        r"""(?:app|router)\.(get|post|put|patch|delete)\(\s*['"]([^'"]+)['"]"""
    )
    fastapi_pattern = re.compile(
        r"""@\w+\.(get|post|put|patch|delete)\(\s*['"]([^'"]+)['"]"""
    )

    for filepath, info in files_map.items():
        content = ''.join(info['content'])

        # Flask
        for match in flask_pattern.finditer(content):
            route = match.group(1)
            methods = match.group(2)
            if methods:
                for method in re.findall(r"'(\w+)'", methods):
                    key = f"{method.upper()} {route}"
                    pos = match.end()
                    handler_match = re.search(r'def\s+(\w+)', content[pos:pos+200])
                    handler = handler_match.group(1) if handler_match else 'unknown'
                    line = content[:match.start()].count('\n') + 1
                    endpoints[key] = {'handler': handler, 'file': filepath, 'line': line}
            else:
                key = f"GET {route}"
                pos = match.end()
                handler_match = re.search(r'def\s+(\w+)', content[pos:pos+200])
                handler = handler_match.group(1) if handler_match else 'unknown'
                line = content[:match.start()].count('\n') + 1
                endpoints[key] = {'handler': handler, 'file': filepath, 'line': line}

        # Express & FastAPI
        for pattern in [express_pattern, fastapi_pattern]:
            for match in pattern.finditer(content):
                method = match.group(1).upper()
                route = match.group(2)
                key = f"{method} {route}"
                line = content[:match.start()].count('\n') + 1
                endpoints[key] = {'handler': 'inline', 'file': filepath, 'line': line}

    vprint(f"Total endpoints extraidos: {len(endpoints)}", level=1)
    return endpoints


def extract_vue_components(files_map):
    """
    Extrae componentes Vue/React con props y emits.
    
    Args:
        files_map: Dict con contenido de archivos
        
    Returns:
        Dict {component_name: {'file': str, 'props': [], 'emits': [], 'api': []}}
    """
    vprint("Extrayendo componentes UI...", level=1)
    
    components = {}

    for filepath, info in files_map.items():
        content = ''.join(info['content'])

        # Detectar nombre del componente
        name_match = re.search(r"name:\s*['\"](\w+)['\"]", content)
        if not name_match:
            if '.vue' in filepath or ('template' in content and ('props' in content or 'setup' in content)):
                name_match = re.search(r"const\s+(\w+)\s*=\s*\{", content)

        if not name_match:
            continue

        comp_name = name_match.group(1)

        # Extraer props
        props = []
        props_match = re.search(r"props:\s*\[([^\]]+)\]", content)
        if props_match:
            props = re.findall(r"['\"](\w+)['\"]", props_match.group(1))
        else:
            props_match = re.search(r"props:\s*\{([^}]+)\}", content, re.DOTALL)
            if props_match:
                props = re.findall(r"(\w+)\s*:", props_match.group(1))

        # Extraer emits
        emits = []
        emits_match = re.search(r"emits:\s*\[([^\]]+)\]", content)
        if emits_match:
            emits = re.findall(r"['\"]([^'\"]+)['\"]", emits_match.group(1))

        # Detectar llamadas API
        api_calls = re.findall(r"""Api\.(?:fetch|getData)\(\s*['"]([^'"]+)['"]""", content)

        if props or emits or 'template' in content:
            components[comp_name] = {
                'file': filepath,
                'props': props,
                'emits': emits,
                'api': api_calls
            }
            vprint(f"{comp_name}: {len(props)} props, {len(emits)} emits, {len(api_calls)} API calls", level=2)

    vprint(f"Total componentes extraidos: {len(components)}", level=1)
    return components


def extract_dependencies(files_map):
    """
    Extrae dependencias entre archivos (que archivo importa cuales otros).
    
    Args:
        files_map: Dict con contenido de archivos
        
    Returns:
        Dict {filepath: [lista_de_archivos_importados]}
    """
    vprint("Mapeando dependencias...", level=1)
    
    deps = {}

    py_import = re.compile(r'^\s*(?:from|import)\s+(\S+)')
    js_import = re.compile(r"""(?:import\s+.*?from\s+|require\s*\(\s*)['"]([^'"]+)['"]""")

    for filepath, info in files_map.items():
        file_deps = set()
        ext = info['type']

        for line in info['content']:
            if ext == 'py':
                m = py_import.match(line)
                if m:
                    module = m.group(1).split('.')[0]
                    for other_path in files_map:
                        if module in other_path and other_path != filepath:
                            file_deps.add(other_path)
                            break
            elif ext in ('js', 'ts', 'tsx', 'jsx', 'vue'):
                m = js_import.search(line)
                if m:
                    imported = m.group(1)
                    if imported.startswith('.'):
                        base_dir = os.path.dirname(filepath)
                        resolved = os.path.normpath(os.path.join(base_dir, imported))
                        
                        for other_path in files_map:
                            if other_path.startswith(resolved):
                                file_deps.add(other_path)
                                break

        if file_deps:
            deps[filepath] = list(file_deps)
            vprint(f"{filepath}: {len(file_deps)} dependencias", level=2)

    vprint(f"Total archivos con dependencias: {len(deps)}", level=1)
    return deps
