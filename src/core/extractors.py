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
    - Python: def, async def, class, @decorator, @dataclass, @property
    - JavaScript/TypeScript: function, arrow functions, class, const func =
    - Go: func, type struct
    - Rust: fn, struct, enum, impl
    - Java: metodos publicos/privados, class, interface
    - Ruby: def, class, module
    - PHP: function, class, trait, interface, namespace
    
    Args:
        files_map: Dict {filepath: {'type': 'py', 'lines': N, 'content': [lines]}}
    
    Returns:
        Dict {filepath: {function_name: line_number}}
        
    Notas:
        - Para Python detecta metodos de clase como "ClassName.method_name"
        - Detecta decoradores Python como "@decorator → function_name"
        - Los numeros de linea son 1-based (primera linea = 1)
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
            (r'^type\s+(\w+)\s+interface', 'interface'),
        ],
        'rs': [
            (r'^\s*(?:pub\s+)?fn\s+(\w+)', 'function'),
            (r'^\s*(?:pub\s+)?struct\s+(\w+)', 'struct'),
            (r'^\s*(?:pub\s+)?enum\s+(\w+)', 'enum'),
            (r'^\s*impl(?:<[^>]+>)?\s+(\w+)', 'impl'),
        ],
        'java': [
            (r'^\s*(?:public|private|protected)?\s*(?:static\s+)?(?:\w+\s+)+(\w+)\s*\(', 'method'),
            (r'^\s*(?:public\s+)?class\s+(\w+)', 'class'),
            (r'^\s*(?:public\s+)?interface\s+(\w+)', 'interface'),
        ],
        'rb': [
            (r'^\s*def\s+(\w+)', 'method'),
            (r'^\s*class\s+(\w+)', 'class'),
            (r'^\s*module\s+(\w+)', 'module'),
        ],
        'php': [
            (r'^\s*(?:public|private|protected)?\s*(?:static\s+)?function\s+(\w+)', 'function'),
            (r'^\s*class\s+(\w+)', 'class'),
            (r'^\s*trait\s+(\w+)', 'trait'),
            (r'^\s*interface\s+(\w+)', 'interface'),
            (r'^\s*namespace\s+([A-Za-z_\\]+)', 'namespace'),
        ],
    }

    # Patrones para decoradores Python
    py_decorator_re = re.compile(r'^\s*@(\w+(?:\.\w+)*)')
    py_dataclass_re = re.compile(r'^\s*@dataclass')
    py_property_re = re.compile(r'^\s*@property')

    for filepath, info in files_map.items():
        ext = info['type']
        pats = patterns.get(ext)
        if pats is None and ext in ('ts', 'tsx', 'jsx'):
            pats = patterns.get('js')
        if not pats:
            continue

        file_funcs = {}
        current_class = None
        pending_decorators = []

        for i, line in enumerate(info['content'], 1):
            # Python: capturar decoradores
            if ext == 'py':
                dec_match = py_decorator_re.match(line)
                if dec_match:
                    decorator = dec_match.group(1)
                    pending_decorators.append(decorator)
                    # Registrar @dataclass y @property como anotaciones especiales
                    continue
            
            for pattern, kind in pats:
                if ext == 'py':
                    m = re.match(pattern, line)
                    if m:
                        indent = len(m.group(1))
                        name = m.group(2)
                        
                        # Agregar prefijo de decorador si es relevante
                        decorator_prefix = ""
                        if pending_decorators:
                            for dec in pending_decorators:
                                if dec in ('dataclass', 'dataclasses.dataclass'):
                                    decorator_prefix = "@dataclass "
                                elif dec == 'property':
                                    decorator_prefix = "@property "
                                elif dec in ('abstractmethod', 'abc.abstractmethod'):
                                    decorator_prefix = "@abstract "
                                elif dec in ('staticmethod',):
                                    decorator_prefix = "@static "
                                elif dec in ('classmethod',):
                                    decorator_prefix = "@classmethod "
                            pending_decorators = []
                        else:
                            pending_decorators = []
                        
                        if kind == 'class':
                            current_class = name
                            display_name = f"{decorator_prefix}{name}" if decorator_prefix else name
                            file_funcs[display_name] = i
                        elif indent > 0 and current_class:
                            display_name = f"{current_class}.{decorator_prefix}{name}" if decorator_prefix else f"{current_class}.{name}"
                            file_funcs[display_name] = i
                        else:
                            current_class = None
                            display_name = f"{decorator_prefix}{name}" if decorator_prefix else name
                            file_funcs[display_name] = i
                        break
                else:
                    m = re.match(pattern, line)
                    if m:
                        name = m.group(1) if m.lastindex else m.group(0).strip()
                        if name and not name.startswith(('if', 'for', 'while', 'switch', 'return', 'else')):
                            file_funcs[name] = i
                        break
            else:
                # Si no hubo match en ningún patrón, resetear decoradores pendientes
                # solo si la línea no es vacía ni comentario
                if ext == 'py' and line.strip() and not line.strip().startswith('#') and not line.strip().startswith('@'):
                    pending_decorators = []

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
    - Django: path() / url() en urls.py
    - Laravel: Route::get / Route::post / etc.
    - NestJS: @Get() / @Post() con @Controller()
    
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
    # Django: path('route/', view, name='...')
    django_path_pattern = re.compile(
        r"""(?:path|re_path)\(\s*['"]([^'"]*)['"]\s*,\s*(\w+(?:\.\w+)*)"""
    )
    # Laravel: Route::get('/route', [Controller::class, 'method']) o Route::get('/route', 'Controller@method')
    laravel_pattern = re.compile(
        r"""Route::(get|post|put|patch|delete|any)\(\s*['"]([^'"]+)['"]"""
    )
    # NestJS: @Get('/route'), @Post('/route')
    nestjs_pattern = re.compile(
        r"""@(Get|Post|Put|Patch|Delete)\(\s*(?:['"]([^'"]*)['"]\s*)?\)"""
    )

    for filepath, info in files_map.items():
        content = ''.join(info['content'])
        ext = info['type']

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
                # Intentar encontrar handler
                pos = match.end()
                handler_match = re.search(r'(?:def|async def|function)\s+(\w+)', content[pos:pos+300])
                handler = handler_match.group(1) if handler_match else 'inline'
                endpoints[key] = {'handler': handler, 'file': filepath, 'line': line}

        # Django urls.py
        if ext == 'py' and ('urls' in filepath.lower() or 'urlpatterns' in content):
            for match in django_path_pattern.finditer(content):
                route = match.group(1)
                handler = match.group(2)
                key = f"ALL /{route}" if route else f"ALL /"
                line = content[:match.start()].count('\n') + 1
                endpoints[key] = {'handler': handler, 'file': filepath, 'line': line}

        # Laravel routes
        if ext == 'php':
            for match in laravel_pattern.finditer(content):
                method = match.group(1).upper()
                route = match.group(2)
                key = f"{method} {route}"
                line = content[:match.start()].count('\n') + 1
                # Intentar encontrar controller
                pos = match.end()
                ctrl_match = re.search(r"""(\w+)(?:::class|@(\w+))""", content[pos:pos+200])
                handler = ctrl_match.group(1) if ctrl_match else 'inline'
                if ctrl_match and ctrl_match.group(2):
                    handler = f"{ctrl_match.group(1)}@{ctrl_match.group(2)}"
                endpoints[key] = {'handler': handler, 'file': filepath, 'line': line}

        # NestJS decorators
        if ext in ('ts', 'js'):
            # Primero detectar el controller
            controller_match = re.search(r"@Controller\(\s*['\"](/[^'\"]*)['\"]", content)
            base_route = controller_match.group(1) if controller_match else ''
            
            for match in nestjs_pattern.finditer(content):
                method = match.group(1).upper()
                route = match.group(2) or ''
                full_route = f"{base_route}/{route}".replace('//', '/')
                key = f"{method} {full_route}"
                line = content[:match.start()].count('\n') + 1
                # Intentar encontrar método handler
                pos = match.end()
                handler_match = re.search(r'(?:async\s+)?(\w+)\s*\(', content[pos:pos+100])
                handler = handler_match.group(1) if handler_match else 'unknown'
                endpoints[key] = {'handler': handler, 'file': filepath, 'line': line}

    vprint(f"Total endpoints extraidos: {len(endpoints)}", level=1)
    return endpoints


def extract_ui_components(files_map):
    """
    Extrae componentes UI de Vue, React y Svelte.
    
    Soporta:
    - Vue: defineComponent, name:, <template>, <script setup>
    - React: function Component, const Component = (), forwardRef, memo
    - React hooks: useState, useEffect, useContext, custom hooks (useXxx)
    - Svelte: archivos .svelte
    
    Args:
        files_map: Dict con contenido de archivos
        
    Returns:
        Dict {component_name: {'file': str, 'props': [], 'emits': [], 'hooks': [], 'type': str}}
    """
    vprint("Extrayendo componentes UI...", level=1)
    
    components = {}

    # Patrones React
    react_func_component = re.compile(
        r"""(?:export\s+)?(?:default\s+)?function\s+([A-Z]\w+)\s*\("""
    )
    react_arrow_component = re.compile(
        r"""(?:export\s+)?(?:default\s+)?const\s+([A-Z]\w+)\s*(?::\s*\w+(?:<[^>]+>)?\s*)?=\s*(?:React\.)?(?:memo|forwardRef)?\s*\(?(?:async\s*)?\("""
    )
    react_hook_pattern = re.compile(r'\buse[A-Z]\w+')
    react_props_pattern = re.compile(r'(?:interface|type)\s+(\w+Props)\s*(?:=\s*)?{([^}]+)}', re.DOTALL)

    for filepath, info in files_map.items():
        content = ''.join(info['content'])
        ext = info['type']

        # === VUE COMPONENTS ===
        if ext == 'vue' or (ext in ('js', 'ts') and ('defineComponent' in content or 'createApp' in content)):
            # Detectar nombre del componente
            name_match = re.search(r"name:\s*['\"](\w+)['\"]", content)
            if not name_match:
                if '.vue' in filepath:
                    # Nombre del archivo sin extensión
                    name_match_fallback = os.path.splitext(os.path.basename(filepath))[0]
                    if name_match_fallback[0].isupper():
                        comp_name = name_match_fallback
                    else:
                        continue
                else:
                    name_match = re.search(r"const\s+(\w+)\s*=\s*(?:defineComponent|createApp)", content)
                    if not name_match:
                        continue
                    comp_name = name_match.group(1)
            else:
                comp_name = name_match.group(1)

            # Extraer props
            props = []
            props_match = re.search(r"(?:defineProps|props)\s*(?:<[^>]+>)?\s*\(\s*\[([^\]]+)\]", content)
            if props_match:
                props = re.findall(r"['\"](\w+)['\"]", props_match.group(1))
            else:
                props_match = re.search(r"(?:defineProps|props)\s*(?:<[^>]+>)?\s*\(\s*\{([^}]+)\}", content, re.DOTALL)
                if not props_match:
                    props_match = re.search(r"props:\s*\{([^}]+)\}", content, re.DOTALL)
                if props_match:
                    props = re.findall(r"(\w+)\s*:", props_match.group(1))

            # Extraer emits
            emits = []
            emits_match = re.search(r"(?:defineEmits|emits)\s*\(\s*\[([^\]]+)\]", content)
            if not emits_match:
                emits_match = re.search(r"emits:\s*\[([^\]]+)\]", content)
            if emits_match:
                emits = re.findall(r"['\"]([^'\"]+)['\"]", emits_match.group(1))

            if props or emits or 'template' in content or '<template' in content:
                components[comp_name] = {
                    'file': filepath,
                    'props': props,
                    'emits': emits,
                    'hooks': [],
                    'type': 'vue'
                }
                vprint(f"Vue: {comp_name}: {len(props)} props, {len(emits)} emits", level=2)

        # === REACT COMPONENTS ===
        elif ext in ('jsx', 'tsx', 'js', 'ts'):
            # Verificar si parece un archivo React
            has_jsx = 'React' in content or 'react' in content or 'jsx' in content or ext in ('jsx', 'tsx')
            if not has_jsx:
                continue

            # Buscar componentes función
            for pattern in [react_func_component, react_arrow_component]:
                for match in pattern.finditer(content):
                    comp_name = match.group(1)
                    
                    # Extraer hooks usados
                    hooks = list(set(react_hook_pattern.findall(content)))
                    
                    # Extraer props de TypeScript interface/type
                    props = []
                    props_match = react_props_pattern.search(content)
                    if props_match:
                        props = re.findall(r'(\w+)\s*[?:]', props_match.group(2))
                    
                    if comp_name not in components:
                        components[comp_name] = {
                            'file': filepath,
                            'props': props,
                            'emits': [],
                            'hooks': hooks[:10],  # máximo 10 hooks
                            'type': 'react'
                        }
                        vprint(f"React: {comp_name}: {len(props)} props, {len(hooks)} hooks", level=2)

        # === SVELTE COMPONENTS ===
        elif ext == 'svelte':
            comp_name = os.path.splitext(os.path.basename(filepath))[0]
            
            # Extraer props (export let)
            props = re.findall(r'export\s+let\s+(\w+)', content)
            
            # Extraer eventos (dispatch)
            emits = re.findall(r"dispatch\(\s*['\"](\w+)['\"]", content)
            
            components[comp_name] = {
                'file': filepath,
                'props': props,
                'emits': emits,
                'hooks': [],
                'type': 'svelte'
            }
            vprint(f"Svelte: {comp_name}: {len(props)} props", level=2)

    vprint(f"Total componentes extraidos: {len(components)}", level=1)
    return components


# Alias de compatibilidad
def extract_vue_components(files_map):
    """Alias de compatibilidad para extract_ui_components"""
    return extract_ui_components(files_map)


def extract_dependencies(files_map):
    """
    Extrae dependencias entre archivos (que archivo importa cuales otros).
    
    Soporta:
    - Python: from X import Y, import X, import X.Y.Z
    - JavaScript/TypeScript: import, require, @/ aliases
    - PHP: use Namespace\\Class, require, include
    
    Args:
        files_map: Dict con contenido de archivos
        
    Returns:
        Dict {filepath: [lista_de_archivos_importados]}
    """
    vprint("Mapeando dependencias...", level=1)
    
    deps = {}

    py_import = re.compile(r'^\s*(?:from\s+(\S+)\s+import|import\s+(\S+))')
    js_import = re.compile(r"""(?:import\s+.*?from\s+|require\s*\(\s*)['"]([^'"]+)['"]""")
    php_use = re.compile(r'^\s*use\s+([A-Za-z_\\]+(?:\\[A-Za-z_]+)*)')
    php_include = re.compile(r"""(?:require|include)(?:_once)?\s*(?:\(\s*)?['"]([^'"]+)['"]""")

    for filepath, info in files_map.items():
        file_deps = set()
        ext = info['type']

        for line in info['content']:
            if ext == 'py':
                m = py_import.match(line)
                if m:
                    module = (m.group(1) or m.group(2)).split('.')[0]
                    # Buscar coincidencia en archivos del proyecto
                    for other_path in files_map:
                        if other_path == filepath:
                            continue
                        # Coincidencia por nombre de módulo
                        other_parts = other_path.replace("\\", "/").replace("/", ".").rstrip(".py")
                        if module in other_parts.split("."):
                            file_deps.add(other_path)
                            break
                        # Coincidencia por subdirectorio
                        if module in other_path.replace("\\", "/"):
                            file_deps.add(other_path)
                            break
                            
            elif ext in ('js', 'ts', 'tsx', 'jsx', 'vue'):
                m = js_import.search(line)
                if m:
                    imported = m.group(1)
                    if imported.startswith('.'):
                        # Imports relativos
                        base_dir = os.path.dirname(filepath)
                        resolved = os.path.normpath(os.path.join(base_dir, imported))
                        
                        for other_path in files_map:
                            if other_path.startswith(resolved):
                                file_deps.add(other_path)
                                break
                    elif imported.startswith('@/') or imported.startswith('~/'):
                        # Aliases: @/ → src/, ~/ → src/
                        alias_path = imported[2:]  # quitar @/ o ~/
                        for other_path in files_map:
                            normalized = other_path.replace("\\", "/")
                            if alias_path in normalized:
                                file_deps.add(other_path)
                                break
                    # Los imports de node_modules se ignoran (no están en files_map)
                    
            elif ext == 'php':
                # PHP use statements
                m = php_use.match(line)
                if m:
                    namespace = m.group(1).replace("\\", "/")
                    # Buscar archivo que coincida con el namespace
                    for other_path in files_map:
                        normalized = other_path.replace("\\", "/")
                        # Comparar última parte del path con última parte del namespace
                        ns_parts = namespace.split("/")
                        if ns_parts[-1].lower() in normalized.lower():
                            file_deps.add(other_path)
                            break
                
                # PHP require/include
                m = php_include.search(line)
                if m:
                    included = m.group(1)
                    if not included.startswith('http'):
                        base_dir = os.path.dirname(filepath)
                        resolved = os.path.normpath(os.path.join(base_dir, included))
                        for other_path in files_map:
                            if other_path == resolved or other_path.endswith(included):
                                file_deps.add(other_path)
                                break

        if file_deps:
            deps[filepath] = sorted(file_deps)
            vprint(f"{filepath}: {len(file_deps)} dependencias", level=2)

    vprint(f"Total archivos con dependencias: {len(deps)}", level=1)
    return deps
