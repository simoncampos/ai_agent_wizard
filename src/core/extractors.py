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


def extract_call_graph(files_map, functions):
    """
    Extrae grafo de llamadas entre funciones (caller → callees).
    
    Analiza el cuerpo de cada función para detectar llamadas a otras funciones
    conocidas del proyecto, produciendo un mapa caller→callees y callee→callers.
    
    Args:
        files_map: Dict con contenido de archivos
        functions: Dict {filepath: {func_name: line_num}} ya extraído
    
    Returns:
        Dict {
            'calls': {func_key: [called_func_keys]},
            'called_by': {func_key: [caller_func_keys]}
        }
        donde func_key = "filepath::func_name"
    """
    vprint("Extrayendo grafo de llamadas...", level=1)
    
    # Construir set de todas las funciones conocidas (nombre simple → func_key)
    all_func_names = {}  # name → [func_keys]
    func_lines = {}      # func_key → (filepath, start_line)
    
    for fpath, funcs in functions.items():
        for fname, line_num in funcs.items():
            # Limpiar nombre: quitar decoradores y prefijos de clase
            clean_name = fname.split('.')[-1] if '.' in fname else fname
            clean_name = clean_name.split(' ')[-1] if ' ' in clean_name else clean_name
            func_key = f"{fpath}::{fname}"
            func_lines[func_key] = (fpath, line_num)
            if clean_name not in all_func_names:
                all_func_names[clean_name] = []
            all_func_names[clean_name].append(func_key)
    
    # Para cada función, analizar su cuerpo buscando llamadas
    calls = {}     # func_key → [called_func_keys]
    called_by = {} # func_key → [caller_func_keys]
    
    call_pattern = re.compile(r'\b(\w+)\s*\(')
    
    # Palabras clave que no son llamadas a funciones
    skip_words = {
        'if', 'for', 'while', 'switch', 'return', 'else', 'elif', 'catch',
        'except', 'print', 'len', 'range', 'str', 'int', 'float', 'list',
        'dict', 'set', 'tuple', 'bool', 'type', 'isinstance', 'hasattr',
        'getattr', 'setattr', 'super', 'self', 'cls', 'None', 'True', 'False',
        'require', 'import', 'from', 'const', 'let', 'var', 'new', 'typeof',
        'throw', 'async', 'await', 'yield', 'not', 'and', 'or', 'in',
    }
    
    for fpath, info in files_map.items():
        if fpath not in functions:
            continue
        content_lines = info.get('content', [])
        if not content_lines:
            continue
        
        # Obtener funciones de este archivo ordenadas por línea
        file_funcs = sorted(functions[fpath].items(), key=lambda x: x[1])
        
        for idx, (fname, start_line) in enumerate(file_funcs):
            # Determinar rango del cuerpo de la función
            if idx + 1 < len(file_funcs):
                end_line = file_funcs[idx + 1][1] - 1
            else:
                end_line = len(content_lines)
            
            func_key = f"{fpath}::{fname}"
            func_calls = set()
            
            # Analizar líneas del cuerpo
            for line_idx in range(start_line, min(end_line, len(content_lines))):
                line = content_lines[line_idx]
                # Ignorar comentarios y strings
                stripped = line.strip()
                if stripped.startswith('#') or stripped.startswith('//') or stripped.startswith('/*'):
                    continue
                
                for match in call_pattern.finditer(line):
                    called_name = match.group(1)
                    if called_name in skip_words or called_name.startswith('_'):
                        continue
                    if called_name in all_func_names:
                        for target_key in all_func_names[called_name]:
                            if target_key != func_key:  # No auto-referencia
                                func_calls.add(target_key)
            
            if func_calls:
                calls[func_key] = sorted(func_calls)
                for target in func_calls:
                    if target not in called_by:
                        called_by[target] = []
                    called_by[target].append(func_key)
    
    # Ordenar called_by
    for key in called_by:
        called_by[key] = sorted(set(called_by[key]))
    
    vprint(f"Grafo: {len(calls)} funciones con llamadas, {len(called_by)} funciones referenciadas", level=1)
    return {'calls': calls, 'called_by': called_by}


def extract_types_and_models(files_map):
    """
    Extrae tipos, interfaces, modelos de datos y sus campos.
    
    Soporta:
    - Python: dataclass fields, TypedDict, Pydantic BaseModel, Django/SQLAlchemy models
    - TypeScript/JavaScript: interface, type alias
    - Go: struct fields
    - Rust: struct fields, enum variants
    - Java: record, class fields
    - PHP: class properties
    
    Args:
        files_map: Dict con contenido de archivos
    
    Returns:
        Dict {type_name: {'file': str, 'line': int, 'kind': str, 'fields': [{'name': str, 'type': str}], 'extends': []}}
    """
    vprint("Extrayendo tipos y modelos...", level=1)
    
    types = {}
    
    for filepath, info in files_map.items():
        ext = info['type']
        content_lines = info.get('content', [])
        if not content_lines:
            continue
        
        if ext == 'py':
            _extract_python_types(filepath, content_lines, types)
        elif ext in ('ts', 'tsx'):
            _extract_ts_types(filepath, content_lines, types)
        elif ext == 'go':
            _extract_go_types(filepath, content_lines, types)
        elif ext == 'rs':
            _extract_rust_types(filepath, content_lines, types)
        elif ext in ('java', 'kt'):
            _extract_java_types(filepath, content_lines, types)
        elif ext == 'php':
            _extract_php_types(filepath, content_lines, types)
    
    vprint(f"Total tipos/modelos extraídos: {len(types)}", level=1)
    return types


def _extract_python_types(filepath, lines, types):
    """Extrae dataclasses, Pydantic models, TypedDict, Django/SQLAlchemy models"""
    is_dataclass = False
    is_model = False
    current_class = None
    current_line = 0
    current_fields = []
    current_extends = []
    current_kind = 'class'
    indent_level = 0
    
    dataclass_re = re.compile(r'^\s*@dataclass')
    class_re = re.compile(r'^(\s*)class\s+(\w+)(?:\(([^)]+)\))?')
    field_re = re.compile(r'^\s+(\w+)\s*[:=]\s*(.*)')
    model_bases = {'BaseModel', 'Model', 'models.Model', 'db.Model', 'Base', 'DeclarativeBase', 'TypedDict', 'NamedTuple'}
    
    for i, line in enumerate(lines, 1):
        if dataclass_re.match(line):
            is_dataclass = True
            continue
        
        m = class_re.match(line)
        if m:
            # Guardar clase anterior si existe
            if current_class and current_fields:
                types[current_class] = {
                    'file': filepath, 'line': current_line, 'kind': current_kind,
                    'fields': current_fields, 'extends': current_extends
                }
            
            indent_level = len(m.group(1))
            class_name = m.group(2)
            bases = m.group(3) or ''
            base_list = [b.strip() for b in bases.split(',') if b.strip()]
            
            is_model = any(b in model_bases or b.endswith('Model') or b.endswith('Base') for b in base_list)
            
            if is_dataclass or is_model or 'TypedDict' in bases:
                current_class = class_name
                current_line = i
                current_fields = []
                current_extends = base_list
                current_kind = 'dataclass' if is_dataclass else ('pydantic' if 'BaseModel' in bases else 
                               ('django_model' if 'models.Model' in bases or 'Model' in bases else
                               ('typed_dict' if 'TypedDict' in bases else 'model')))
            else:
                current_class = None
            
            is_dataclass = False
            continue
        
        # Extraer campos de la clase actual
        if current_class:
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and not stripped.startswith('def ') and not stripped.startswith('class '):
                fm = field_re.match(line)
                if fm:
                    field_name = fm.group(1)
                    field_type = fm.group(2).split('#')[0].split('=')[0].strip().rstrip(',')
                    if field_name not in ('self', 'cls', 'Meta', '__') and not field_name.startswith('_'):
                        current_fields.append({'name': field_name, 'type': field_type or 'Any'})
            elif not stripped:
                pass  # Línea vacía, continuar
            elif not line.startswith(' ' * (indent_level + 1)):
                # Salimos del bloque de la clase
                if current_fields:
                    types[current_class] = {
                        'file': filepath, 'line': current_line, 'kind': current_kind,
                        'fields': current_fields, 'extends': current_extends
                    }
                current_class = None
    
    # Última clase
    if current_class and current_fields:
        types[current_class] = {
            'file': filepath, 'line': current_line, 'kind': current_kind,
            'fields': current_fields, 'extends': current_extends
        }


def _extract_ts_types(filepath, lines, types):
    """Extrae interfaces y type aliases de TypeScript"""
    interface_re = re.compile(r'^\s*(?:export\s+)?interface\s+(\w+)(?:\s+extends\s+([^{]+))?\s*\{')
    type_re = re.compile(r'^\s*(?:export\s+)?type\s+(\w+)\s*=\s*\{')
    field_re = re.compile(r'^\s+(\w+)(\?)?:\s*(.+?)[;,]?\s*$')
    
    current_type = None
    current_line = 0
    current_fields = []
    current_extends = []
    current_kind = 'interface'
    brace_depth = 0
    
    for i, line in enumerate(lines, 1):
        if current_type is None:
            m = interface_re.match(line)
            if m:
                current_type = m.group(1)
                current_line = i
                current_extends = [e.strip() for e in (m.group(2) or '').split(',') if e.strip()]
                current_kind = 'interface'
                current_fields = []
                brace_depth = line.count('{') - line.count('}')
                continue
            
            m = type_re.match(line)
            if m:
                current_type = m.group(1)
                current_line = i
                current_extends = []
                current_kind = 'type'
                current_fields = []
                brace_depth = line.count('{') - line.count('}')
                continue
        else:
            brace_depth += line.count('{') - line.count('}')
            
            fm = field_re.match(line)
            if fm:
                field_name = fm.group(1)
                optional = fm.group(2) == '?'
                field_type = fm.group(3).strip().rstrip(';,')
                current_fields.append({
                    'name': field_name,
                    'type': f"{field_type}{'?' if optional else ''}"
                })
            
            if brace_depth <= 0:
                if current_fields:
                    types[current_type] = {
                        'file': filepath, 'line': current_line, 'kind': current_kind,
                        'fields': current_fields, 'extends': current_extends
                    }
                current_type = None
    
    if current_type and current_fields:
        types[current_type] = {
            'file': filepath, 'line': current_line, 'kind': current_kind,
            'fields': current_fields, 'extends': current_extends
        }


def _extract_go_types(filepath, lines, types):
    """Extrae struct fields de Go"""
    struct_re = re.compile(r'^type\s+(\w+)\s+struct\s*\{')
    field_re = re.compile(r'^\s+(\w+)\s+(\S+)')
    
    current_type = None
    current_line = 0
    current_fields = []
    
    for i, line in enumerate(lines, 1):
        if current_type is None:
            m = struct_re.match(line)
            if m:
                current_type = m.group(1)
                current_line = i
                current_fields = []
        else:
            if line.strip() == '}':
                if current_fields:
                    types[current_type] = {
                        'file': filepath, 'line': current_line, 'kind': 'struct',
                        'fields': current_fields, 'extends': []
                    }
                current_type = None
            else:
                fm = field_re.match(line)
                if fm and not line.strip().startswith('//'):
                    current_fields.append({'name': fm.group(1), 'type': fm.group(2)})


def _extract_rust_types(filepath, lines, types):
    """Extrae struct fields y enum variants de Rust"""
    struct_re = re.compile(r'^\s*(?:pub\s+)?struct\s+(\w+)')
    enum_re = re.compile(r'^\s*(?:pub\s+)?enum\s+(\w+)')
    field_re = re.compile(r'^\s+(?:pub\s+)?(\w+):\s*(.+?),?\s*$')
    variant_re = re.compile(r'^\s+(\w+)')
    
    current_type = None
    current_line = 0
    current_fields = []
    current_kind = 'struct'
    brace_depth = 0
    
    for i, line in enumerate(lines, 1):
        if current_type is None:
            m = struct_re.match(line)
            if m and '{' in line:
                current_type = m.group(1)
                current_line = i
                current_fields = []
                current_kind = 'struct'
                brace_depth = line.count('{') - line.count('}')
                continue
            m = enum_re.match(line)
            if m and '{' in line:
                current_type = m.group(1)
                current_line = i
                current_fields = []
                current_kind = 'enum'
                brace_depth = line.count('{') - line.count('}')
                continue
        else:
            brace_depth += line.count('{') - line.count('}')
            if current_kind == 'struct':
                fm = field_re.match(line)
                if fm:
                    current_fields.append({'name': fm.group(1), 'type': fm.group(2).rstrip(',')})
            else:
                vm = variant_re.match(line)
                if vm and not line.strip().startswith('//'):
                    name = vm.group(1)
                    if name not in ('}',):
                        current_fields.append({'name': name, 'type': 'variant'})
            
            if brace_depth <= 0:
                if current_fields:
                    types[current_type] = {
                        'file': filepath, 'line': current_line, 'kind': current_kind,
                        'fields': current_fields, 'extends': []
                    }
                current_type = None


def _extract_java_types(filepath, lines, types):
    """Extrae class fields y record de Java/Kotlin"""
    class_re = re.compile(r'^\s*(?:public\s+)?(?:record|class)\s+(\w+)(?:\s+extends\s+(\w+))?')
    field_re = re.compile(r'^\s+(?:private|public|protected)\s+(?:static\s+)?(?:final\s+)?(\w+(?:<[^>]+>)?)\s+(\w+)')
    
    current_type = None
    current_line = 0
    current_fields = []
    current_extends = []
    brace_depth = 0
    
    for i, line in enumerate(lines, 1):
        if current_type is None:
            m = class_re.match(line)
            if m:
                current_type = m.group(1)
                current_line = i
                current_fields = []
                current_extends = [m.group(2)] if m.group(2) else []
                brace_depth = line.count('{') - line.count('}')
        else:
            brace_depth += line.count('{') - line.count('}')
            fm = field_re.match(line)
            if fm:
                current_fields.append({'name': fm.group(2), 'type': fm.group(1)})
            if brace_depth <= 0:
                if current_fields:
                    types[current_type] = {
                        'file': filepath, 'line': current_line, 'kind': 'class',
                        'fields': current_fields, 'extends': current_extends
                    }
                current_type = None


def _extract_php_types(filepath, lines, types):
    """Extrae class properties de PHP"""
    class_re = re.compile(r'^\s*class\s+(\w+)(?:\s+extends\s+(\w+))?')
    prop_re = re.compile(r'^\s+(?:public|private|protected)\s+(?:\??\w+\s+)?\$(\w+)')
    
    current_type = None
    current_line = 0
    current_fields = []
    current_extends = []
    brace_depth = 0
    
    for i, line in enumerate(lines, 1):
        if current_type is None:
            m = class_re.match(line)
            if m:
                current_type = m.group(1)
                current_line = i
                current_fields = []
                current_extends = [m.group(2)] if m.group(2) else []
                brace_depth = line.count('{') - line.count('}')
        else:
            brace_depth += line.count('{') - line.count('}')
            pm = prop_re.match(line)
            if pm:
                current_fields.append({'name': pm.group(1), 'type': 'mixed'})
            if brace_depth <= 0:
                if current_fields:
                    types[current_type] = {
                        'file': filepath, 'line': current_line, 'kind': 'class',
                        'fields': current_fields, 'extends': current_extends
                    }
                current_type = None


def extract_docstrings(files_map, functions):
    """
    Extrae docstrings/JSDoc por función con parámetros y return type.
    
    Solo extrae documentación de funciones que YA tienen docstring/JSDoc.
    No inventa documentación.
    
    Args:
        files_map: Dict con contenido de archivos
        functions: Dict {filepath: {func_name: line_num}}
    
    Returns:
        Dict {func_key: {'file': str, 'line': int, 'description': str, 
                         'params': [{'name': str, 'type': str, 'desc': str}],
                         'returns': {'type': str, 'desc': str}}}
    """
    vprint("Extrayendo docstrings...", level=1)
    
    docstrings = {}
    
    param_re = re.compile(r'^\s*(?::param|@param|Args:)\s*(\w+)(?:\s*\((\w+)\))?\s*:?\s*(.*)')
    param_jsdoc_re = re.compile(r'^\s*\*?\s*@param\s+\{([^}]+)\}\s+(\w+)\s*-?\s*(.*)')
    return_re = re.compile(r'^\s*(?::returns?|@returns?|Returns:)\s*(?:\{([^}]+)\})?\s*:?\s*(.*)')
    
    for filepath, info in files_map.items():
        if filepath not in functions:
            continue
        content_lines = info.get('content', [])
        if not content_lines:
            continue
        
        ext = info['type']
        file_funcs = sorted(functions[filepath].items(), key=lambda x: x[1])
        
        for idx, (fname, start_line) in enumerate(file_funcs):
            if start_line > len(content_lines):
                continue
            
            # Buscar docstring en las líneas siguientes a la definición
            doc_lines = []
            in_doc = False
            doc_start = start_line  # 1-based, así que content_lines[start_line] es la siguiente
            
            if ext == 'py':
                # Buscar triple-quote docstring
                for j in range(start_line, min(start_line + 3, len(content_lines))):
                    line = content_lines[j]
                    if '"""' in line or "'''" in line:
                        in_doc = True
                        doc_start = j
                        break
                
                if in_doc:
                    quote = '"""' if '"""' in content_lines[doc_start] else "'''"
                    # Si abre y cierra en la misma línea
                    if content_lines[doc_start].count(quote) >= 2:
                        doc_lines = [content_lines[doc_start].split(quote)[1]]
                    else:
                        for j in range(doc_start, min(doc_start + 30, len(content_lines))):
                            doc_lines.append(content_lines[j])
                            if j > doc_start and quote in content_lines[j]:
                                break
            
            elif ext in ('js', 'ts', 'tsx', 'jsx'):
                # Buscar JSDoc /** ... */ ANTES de la función
                for j in range(max(0, start_line - 15), start_line - 1):
                    line = content_lines[j]
                    if '/**' in line:
                        for k in range(j, start_line):
                            doc_lines.append(content_lines[k])
                            if '*/' in content_lines[k] and k > j:
                                break
                        break
            
            if not doc_lines:
                continue
            
            # Parsear docstring
            doc_text = ''.join(doc_lines)
            # Limpiar
            doc_text_clean = doc_text.replace('"""', '').replace("'''", '').replace('/**', '').replace('*/', '').strip()
            doc_first_line = doc_text_clean.split('\n')[0].strip().lstrip('* ').strip()
            
            if not doc_first_line or len(doc_first_line) < 3:
                continue
            
            # Extraer params
            params = []
            for line in doc_lines:
                line_str = line if isinstance(line, str) else str(line)
                pm = param_jsdoc_re.match(line_str) or param_re.match(line_str)
                if pm:
                    groups = pm.groups()
                    if len(groups) >= 3:
                        params.append({
                            'name': groups[1] if groups[1] else groups[0],
                            'type': groups[0] if param_jsdoc_re.match(line_str) else (groups[1] or ''),
                            'desc': groups[2] or ''
                        })
            
            # Extraer returns
            returns = None
            for line in doc_lines:
                line_str = line if isinstance(line, str) else str(line)
                rm = return_re.match(line_str)
                if rm:
                    returns = {'type': rm.group(1) or '', 'desc': rm.group(2) or ''}
            
            func_key = f"{filepath}::{fname}"
            docstrings[func_key] = {
                'file': filepath,
                'line': start_line,
                'description': doc_first_line[:150],
                'params': params,
                'returns': returns
            }
    
    vprint(f"Total docstrings extraídos: {len(docstrings)}", level=1)
    return docstrings


def extract_config_map(files_map, project_path):
    """
    Extrae variables de entorno, archivos de configuración y constantes.
    
    Detecta:
    - Variables de entorno referenciadas en código (os.environ, process.env, etc.)
    - Archivos .env, .env.example, config.yaml, settings.py
    - Constantes de configuración
    
    Args:
        files_map: Dict con contenido de archivos
        project_path: Ruta del proyecto
    
    Returns:
        Dict {
            'env_vars': [{'name': str, 'file': str, 'line': int, 'default': str}],
            'config_files': [{'path': str, 'type': str}],
        }
    """
    vprint("Extrayendo mapa de configuración...", level=1)
    
    env_vars = []
    seen_vars = set()
    
    # Patrones para detectar variables de entorno
    patterns = [
        # Python: os.environ['KEY'], os.environ.get('KEY', default), os.getenv('KEY')
        re.compile(r"""os\.environ(?:\.get)?\s*\(\s*['\"](\w+)['\"](?:\s*,\s*['\"]?([^'\")\s]+))?"""),
        re.compile(r"""os\.environ\s*\[\s*['\"](\w+)['\"]\s*\]"""),
        re.compile(r"""os\.getenv\s*\(\s*['\"](\w+)['\"](?:\s*,\s*['\"]?([^'\")\s]+))?"""),
        # JavaScript: process.env.KEY, process.env['KEY']
        re.compile(r"""process\.env\.(\w+)"""),
        re.compile(r"""process\.env\s*\[\s*['\"](\w+)['\"]\s*\]"""),
        # PHP: env('KEY', default), getenv('KEY'), $_ENV['KEY']
        re.compile(r"""env\s*\(\s*['\"](\w+)['\"](?:\s*,\s*['\"]?([^'\")\s]+))?"""),
        re.compile(r"""getenv\s*\(\s*['\"](\w+)['\"]"""),
        re.compile(r"""\$_ENV\s*\[\s*['\"](\w+)['\"]\s*\]"""),
        # Rust: std::env::var("KEY")
        re.compile(r"""env::var\s*\(\s*['\"](\w+)['\"]"""),
        # Go: os.Getenv("KEY")
        re.compile(r"""os\.Getenv\s*\(\s*['\"](\w+)['\"]"""),
    ]
    
    for filepath, info in files_map.items():
        content_lines = info.get('content', [])
        if not content_lines:
            continue
        
        for i, line in enumerate(content_lines, 1):
            for pattern in patterns:
                for match in pattern.finditer(line):
                    var_name = match.group(1)
                    default_val = match.group(2) if match.lastindex and match.lastindex >= 2 else ''
                    if var_name not in seen_vars:
                        seen_vars.add(var_name)
                        env_vars.append({
                            'name': var_name,
                            'file': filepath,
                            'line': i,
                            'default': default_val or ''
                        })
    
    # Detectar archivos de configuración
    config_files = []
    config_patterns = [
        '.env', '.env.example', '.env.local', '.env.production', '.env.development',
        'config.yaml', 'config.yml', 'config.json', 'config.toml',
        'settings.py', 'settings.json', 'appsettings.json',
        '.flaskenv', 'docker-compose.yml', 'docker-compose.yaml',
        'pyproject.toml', 'tsconfig.json', 'webpack.config.js', 'vite.config.ts',
        'vite.config.js', 'next.config.js', 'next.config.mjs', 'nuxt.config.ts',
    ]
    
    for cfg in config_patterns:
        full_path = os.path.join(project_path, cfg)
        if os.path.exists(full_path):
            config_files.append({'path': cfg, 'type': os.path.splitext(cfg)[1].lstrip('.') or 'env'})
    
    vprint(f"Variables de entorno: {len(env_vars)}, Archivos config: {len(config_files)}", level=1)
    return {'env_vars': env_vars, 'config_files': config_files}


def extract_patterns(files_map, functions, frameworks):
    """
    Detecta patrones de diseño y convenciones reales del código.
    
    Detecta:
    - Middleware chains (Express, Django, Laravel)
    - Decoradores como patrones (auth, cache, logging)
    - Singleton, Factory, Repository patterns
    - Error handling strategy
    - Naming conventions detectadas
    - Auth patterns (JWT, session, OAuth)
    
    Args:
        files_map: Dict con contenido de archivos
        functions: Dict de funciones extraídas
        frameworks: Dict de frameworks detectados
    
    Returns:
        Dict con patrones detectados por categoría
    """
    vprint("Detectando patrones de diseño...", level=1)
    
    result = {
        'middleware': [],
        'decorators': {},
        'design_patterns': [],
        'error_handling': {'strategy': 'distributed', 'custom_exceptions': []},
        'naming': {'style': 'unknown', 'samples': {}},
        'auth': [],
    }
    
    all_func_names = []
    decorator_counts = {}
    has_centralized_error = False
    custom_exceptions = set()
    
    for filepath, info in files_map.items():
        ext = info['type']
        content_lines = info.get('content', [])
        if not content_lines:
            continue
        
        content = ''.join(content_lines)
        
        # --- Middleware detection ---
        if ext == 'py':
            # Django middleware
            for i, line in enumerate(content_lines, 1):
                if 'MIDDLEWARE' in line and '=' in line:
                    result['middleware'].append({'type': 'django', 'file': filepath, 'line': i})
                if re.match(r'^\s*class\s+\w+Middleware', line):
                    name = re.match(r'^\s*class\s+(\w+Middleware)', line).group(1)
                    result['middleware'].append({'type': 'custom', 'name': name, 'file': filepath, 'line': i})
            
            # Detectar decoradores
            for i, line in enumerate(content_lines, 1):
                dm = re.match(r'^\s*@(\w+(?:\.\w+)*)', line)
                if dm:
                    dec = dm.group(1)
                    if dec not in ('property', 'staticmethod', 'classmethod', 'abstractmethod', 'dataclass'):
                        decorator_counts[dec] = decorator_counts.get(dec, 0) + 1
            
            # Custom exceptions
            for line in content_lines:
                em = re.match(r'^\s*class\s+(\w*(?:Error|Exception))\s*\(', line)
                if em:
                    custom_exceptions.add(em.group(1))
        
        elif ext in ('js', 'ts', 'tsx', 'jsx'):
            # Express middleware
            for i, line in enumerate(content_lines, 1):
                if re.search(r'app\.use\(', line):
                    result['middleware'].append({'type': 'express', 'file': filepath, 'line': i})
        
        elif ext == 'php':
            # Laravel middleware
            for i, line in enumerate(content_lines, 1):
                if re.search(r'->middleware\(', line):
                    result['middleware'].append({'type': 'laravel', 'file': filepath, 'line': i})
        
        # --- Auth patterns ---
        auth_keywords = {
            'jwt': ['jwt', 'jsonwebtoken', 'JWT_SECRET', 'jwt.sign', 'jwt.verify', 'JWTAuth', 'PyJWT'],
            'session': ['session', 'SESSION_SECRET', 'express-session', 'session_start', 'SessionMiddleware'],
            'oauth': ['oauth', 'OAuth', 'passport', 'social_auth', 'allauth', 'Socialite'],
        }
        content_lower = content.lower()
        for auth_type, keywords in auth_keywords.items():
            if any(kw.lower() in content_lower for kw in keywords):
                if auth_type not in result['auth']:
                    result['auth'].append(auth_type)
        
        # --- Error handling ---
        if 'error_handler' in content.lower() or 'errorhandler' in content.lower() or 'exception_handler' in content.lower():
            has_centralized_error = True
        
        # --- Collect function names for naming analysis ---
        if filepath in functions:
            all_func_names.extend(functions[filepath].keys())
    
    # --- Design patterns ---
    for filepath, info in files_map.items():
        content = ''.join(info.get('content', []))
        basename = os.path.basename(filepath).lower()
        
        if 'singleton' in content.lower() or '_instance' in content:
            result['design_patterns'].append('singleton')
        if 'factory' in basename or 'Factory' in content:
            result['design_patterns'].append('factory')
        if 'repository' in basename or 'Repository' in content:
            result['design_patterns'].append('repository')
        if 'service' in basename:
            result['design_patterns'].append('service_layer')
    
    result['design_patterns'] = sorted(set(result['design_patterns']))
    
    # --- Analyze naming conventions ---
    snake_count = sum(1 for n in all_func_names if '_' in n and n.islower())
    camel_count = sum(1 for n in all_func_names if not '_' in n and n[0].islower() if len(n) > 1)
    pascal_count = sum(1 for n in all_func_names if n[0:1].isupper() and not '_' in n if len(n) > 1)
    
    if snake_count > camel_count and snake_count > pascal_count:
        result['naming']['style'] = 'snake_case'
    elif camel_count > snake_count:
        result['naming']['style'] = 'camelCase'
    result['naming']['samples'] = {
        'snake_case': snake_count, 'camelCase': camel_count, 'PascalCase': pascal_count
    }
    
    # --- Decorators summary ---
    top_decorators = sorted(decorator_counts.items(), key=lambda x: -x[1])[:10]
    result['decorators'] = {k: v for k, v in top_decorators}
    
    # --- Error handling ---
    result['error_handling']['strategy'] = 'centralized' if has_centralized_error else 'distributed'
    result['error_handling']['custom_exceptions'] = sorted(custom_exceptions)
    
    vprint(f"Patrones: {len(result['design_patterns'])} diseño, {len(result['middleware'])} middleware, {len(result['auth'])} auth", level=1)
    return result


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
