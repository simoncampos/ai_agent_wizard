"""
Tests unitarios del AI Agent Wizard v4.0.0
"""

import unittest
import tempfile
import os
import shutil
import sys

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.validators import check_python_version, check_git_installed, check_disk_space, check_write_permissions
from core.scanner import scan_files, is_empty_project
from core.detectors import detect_languages, detect_frameworks
from core.extractors import extract_functions, extract_endpoints, extract_ui_components, extract_dependencies
from templates.project_templates import suggest_template
from generators.all_generators import (
    generate_project_index, generate_all_yamls,
    generate_architecture_yaml, generate_flow_yaml, generate_graph_yaml,
    generate_changes_yaml, generate_summaries_yaml,
    generate_context_budget_yaml, generate_protocol_yaml
)


class TestValidators(unittest.TestCase):
    """Tests para validadores"""
    
    def test_python_version(self):
        """Verifica que Python 3.7+ esta instalado"""
        ok, msg = check_python_version()
        self.assertTrue(ok, "Debe tener Python 3.7+")
    
    def test_git_installed(self):
        """Verifica que Git esta instalado"""
        ok, msg = check_git_installed()
        self.assertTrue(ok, "Git debe estar instalado")

    def test_disk_space(self):
        """Verifica que check_disk_space funciona en Windows"""
        ok, msg = check_disk_space(tempfile.gettempdir())
        self.assertTrue(ok, "Debe haber espacio en disco")
        self.assertIn("disponibles", msg)
    
    def test_write_permissions(self):
        """Verifica permisos de escritura"""
        ok, msg = check_write_permissions(tempfile.gettempdir())
        self.assertTrue(ok, "Debe tener permisos de escritura en temp")


class TestScanner(unittest.TestCase):
    """Tests para el escaner de archivos"""
    
    def setUp(self):
        """Crea directorio temporal para tests"""
        self.tmpdir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Limpia directorio temporal"""
        shutil.rmtree(self.tmpdir)
    
    def test_is_empty_project(self):
        """Detecta directorio vacio"""
        self.assertTrue(is_empty_project(self.tmpdir))
        
        # Agregar archivo oculto
        open(os.path.join(self.tmpdir, '.hidden'), 'w').close()
        self.assertTrue(is_empty_project(self.tmpdir))
        
        # Agregar archivo normal
        open(os.path.join(self.tmpdir, 'file.txt'), 'w').close()
        self.assertFalse(is_empty_project(self.tmpdir))
    
    def test_scan_files(self):
        """Escanea archivos correctamente"""
        test_file = os.path.join(self.tmpdir, 'test.py')
        with open(test_file, 'w') as f:
            f.write('def test():\n    pass\n')
        
        files_map = scan_files(self.tmpdir)
        self.assertEqual(len(files_map), 1)
        self.assertIn('test.py', files_map)
        self.assertEqual(files_map['test.py']['type'], 'py')
        self.assertEqual(files_map['test.py']['lines'], 2)


class TestDetectors(unittest.TestCase):
    """Tests para detectores"""
    
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.tmpdir)
    
    def test_detect_languages(self):
        """Detecta lenguajes por extension"""
        # Crear archivos de prueba
        open(os.path.join(self.tmpdir, 'test.py'), 'w').close()
        open(os.path.join(self.tmpdir, 'app.js'), 'w').close()
        
        from core.scanner import iter_source_files
        languages = detect_languages(self.tmpdir, iter_source_files(self.tmpdir))
        
        self.assertIn('Python', languages)
        self.assertIn('JavaScript', languages)

    def test_detect_frameworks_django(self):
        """Detecta Django por manage.py y requirements.txt"""
        open(os.path.join(self.tmpdir, 'manage.py'), 'w').close()
        with open(os.path.join(self.tmpdir, 'requirements.txt'), 'w') as f:
            f.write('django==4.2\ndjango-cors-headers\n')
        
        frameworks = detect_frameworks(self.tmpdir)
        self.assertIn('Django', frameworks['backend'])

    def test_detect_frameworks_laravel(self):
        """Detecta Laravel por artisan"""
        open(os.path.join(self.tmpdir, 'artisan'), 'w').close()
        
        frameworks = detect_frameworks(self.tmpdir)
        self.assertIn('Laravel', frameworks['backend'])
    
    def test_detect_frameworks_react(self):
        """Detecta React por package.json"""
        import json
        pkg = {'dependencies': {'react': '^18.0.0'}}
        with open(os.path.join(self.tmpdir, 'package.json'), 'w') as f:
            json.dump(pkg, f)
        
        frameworks = detect_frameworks(self.tmpdir)
        self.assertIn('React', frameworks['frontend'])


class TestExtractors(unittest.TestCase):
    """Tests para extractores"""
    
    def test_extract_python_functions(self):
        """Extrae funciones y clases de Python"""
        files_map = {
            'test.py': {
                'type': 'py',
                'lines': 5,
                'content': [
                    'def funcion_uno():\n',
                    '    pass\n',
                    '\n',
                    'class MiClase:\n',
                    '    pass\n'
                ]
            }
        }
        
        functions = extract_functions(files_map)
        
        self.assertIn('test.py', functions)
        self.assertIn('funcion_uno', functions['test.py'])
        self.assertIn('MiClase', functions['test.py'])
        self.assertEqual(functions['test.py']['funcion_uno'], 1)
        self.assertEqual(functions['test.py']['MiClase'], 4)
    
    def test_extract_python_decorators(self):
        """Extrae funciones con decoradores"""
        files_map = {
            'models.py': {
                'type': 'py',
                'lines': 4,
                'content': [
                    '@dataclass\n',
                    'class User:\n',
                    '    name: str\n',
                    '    age: int\n'
                ]
            }
        }
        
        functions = extract_functions(files_map)
        self.assertIn('models.py', functions)
        # Should detect the dataclass-decorated class
        found_dataclass = any('@dataclass' in k for k in functions['models.py'])
        self.assertTrue(found_dataclass, "Debe detectar decorador @dataclass")

    def test_extract_php_functions(self):
        """Extrae funciones y clases de PHP"""
        files_map = {
            'Controller.php': {
                'type': 'php',
                'lines': 6,
                'content': [
                    '<?php\n',
                    'namespace App\\Controllers;\n',
                    '\n',
                    'class UserController {\n',
                    '    public function index() {\n',
                    '    }\n'
                ]
            }
        }
        
        functions = extract_functions(files_map)
        self.assertIn('Controller.php', functions)
        self.assertIn('UserController', functions['Controller.php'])
        self.assertIn('index', functions['Controller.php'])

    def test_extract_js_functions(self):
        """Extrae funciones JavaScript"""
        files_map = {
            'app.js': {
                'type': 'js',
                'lines': 4,
                'content': [
                    'function handleClick() {\n',
                    '}\n',
                    'const fetchData = async () => {\n',
                    '}\n'
                ]
            }
        }
        
        functions = extract_functions(files_map)
        self.assertIn('app.js', functions)
        self.assertIn('handleClick', functions['app.js'])
        self.assertIn('fetchData', functions['app.js'])
    
    def test_extract_flask_endpoints(self):
        """Extrae endpoints Flask"""
        files_map = {
            'routes.py': {
                'type': 'py',
                'lines': 4,
                'content': [
                    "@app.route('/users', methods=['GET', 'POST'])\n",
                    'def get_users():\n',
                    '    pass\n',
                    '\n'
                ]
            }
        }
        
        endpoints = extract_endpoints(files_map)
        self.assertIn('GET /users', endpoints)
        self.assertIn('POST /users', endpoints)

    def test_extract_express_endpoints(self):
        """Extrae endpoints Express"""
        files_map = {
            'routes.js': {
                'type': 'js',
                'lines': 3,
                'content': [
                    "app.get('/api/users', (req, res) => {\n",
                    "});\n",
                    "app.post('/api/users', createUser);\n"
                ]
            }
        }
        
        endpoints = extract_endpoints(files_map)
        self.assertIn('GET /api/users', endpoints)
        self.assertIn('POST /api/users', endpoints)

    def test_extract_laravel_endpoints(self):
        """Extrae endpoints Laravel"""
        files_map = {
            'web.php': {
                'type': 'php',
                'lines': 3,
                'content': [
                    "Route::get('/users', [UserController::class, 'index']);\n",
                    "Route::post('/users', [UserController::class, 'store']);\n",
                    "\n"
                ]
            }
        }
        
        endpoints = extract_endpoints(files_map)
        self.assertIn('GET /users', endpoints)
        self.assertIn('POST /users', endpoints)

    def test_extract_django_endpoints(self):
        """Extrae endpoints Django"""
        files_map = {
            'urls.py': {
                'type': 'py',
                'lines': 5,
                'content': [
                    'from django.urls import path\n',
                    'urlpatterns = [\n',
                    "    path('users/', views.user_list),\n",
                    "    path('users/<int:pk>/', views.user_detail),\n",
                    ']\n'
                ]
            }
        }
        
        endpoints = extract_endpoints(files_map)
        self.assertTrue(len(endpoints) >= 2, f"Debe extraer al menos 2 endpoints Django, encontrados: {len(endpoints)}")
    
    def test_extract_dependencies_python(self):
        """Extrae dependencias Python"""
        files_map = {
            'main.py': {
                'type': 'py',
                'lines': 2,
                'content': [
                    'from utils import helpers\n',
                    'import os\n'
                ]
            },
            'utils/helpers.py': {
                'type': 'py',
                'lines': 1,
                'content': ['def help(): pass\n']
            }
        }
        
        deps = extract_dependencies(files_map)
        self.assertIn('main.py', deps)
        self.assertIn('utils/helpers.py', deps['main.py'])


class TestGenerators(unittest.TestCase):
    """Tests para generadores de YAML"""
    
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.project_name = 'test_project'
        self.languages = ['Python']
        self.frameworks = {'backend': ['Flask'], 'frontend': [], 'db': [], 'other': []}
        self.files_map = {
            'app.py': {'type': 'py', 'lines': 10},
            'utils.py': {'type': 'py', 'lines': 5}
        }
        self.functions = {'app.py': {'create_app': 1, 'main': 8}}
        self.endpoints = {'GET /api/users': {'handler': 'get_users', 'file': 'app.py', 'line': 5}}
        self.components = {}
        self.dependencies = {'app.py': ['utils.py']}
    
    def tearDown(self):
        shutil.rmtree(self.tmpdir)
    
    def test_generate_project_index(self):
        """Genera PROJECT_INDEX.yaml con datos del proyecto"""
        files_map = {
            'app.py': {'type': 'py', 'lines': 10},
            'utils.py': {'type': 'py', 'lines': 5}
        }
        content = generate_project_index(
            self.tmpdir, self.project_name, self.languages, self.frameworks,
            files_map, self.functions, self.endpoints, self.components, self.dependencies
        )
        self.assertIn('TEST_PROJECT', content)
        self.assertIn('app.py', content)
        self.assertIn('create_app', content)
        self.assertIn('GET /api/users', content)
    
    def test_generate_architecture_yaml(self):
        """Genera ARCHITECTURE.yaml dinámico"""
        content = generate_architecture_yaml(
            self.tmpdir, self.languages, self.frameworks,
            self.files_map, self.functions, self.dependencies
        )
        self.assertIn('ARCHITECTURE', content)
        self.assertIn('optimizer_purpose', content)
        # No debe contener referencia al wizard (era el bug de hardcodear)
        self.assertNotIn('core.scanner', content)
    
    def test_generate_graph_yaml(self):
        """Genera GRAPH.yaml con datos reales"""
        content = generate_graph_yaml(
            self.dependencies, self.functions, self.endpoints, self.components
        )
        self.assertIn('DEPENDENCY GRAPH', content)
        self.assertIn('total_functions: 2', content)
        self.assertIn('total_endpoints: 1', content)
    
    def test_generate_changes_yaml(self):
        """Genera CHANGES.yaml con tracking de hashes"""
        files_map = {
            'app.py': {'type': 'py', 'lines': 2, 'content': ['def main(): pass\n', '\n']}
        }
        content = generate_changes_yaml(self.tmpdir, files_map)
        self.assertIn('CHANGES', content)
        self.assertIn('total_files: 1', content)
        # Verificar que se creó .state.json
        state_file = os.path.join(self.tmpdir, '.ai', '.state.json')
        self.assertTrue(os.path.exists(state_file))
    
    def test_generate_summaries_yaml(self):
        """Genera SUMMARIES.yaml con resúmenes"""
        files_map = {
            'app.py': {
                'type': 'py', 'lines': 3,
                'content': ['"""Flask application."""\n', 'def create_app():\n', '    pass\n']
            }
        }
        content = generate_summaries_yaml(files_map, self.functions)
        self.assertIn('SUMMARIES', content)
        self.assertIn('app.py', content)
    
    def test_generate_context_budget_yaml(self):
        """Genera CONTEXT_BUDGET.yaml con prioridades"""
        content = generate_context_budget_yaml(
            self.files_map, self.functions, self.endpoints, self.components
        )
        self.assertIn('CONTEXT BUDGET', content)
        self.assertIn('critical', content)
    
    def test_generate_protocol_yaml(self):
        """Genera PROTOCOL.yaml"""
        content = generate_protocol_yaml()
        self.assertIn('PROTOCOL', content)
        self.assertIn('read_order', content)
        self.assertIn('modification_rules', content)
    
    def test_generate_all_yamls(self):
        """Genera todos los YAMLs básicos"""
        yamls = generate_all_yamls(
            self.project_name, self.languages, self.frameworks,
            self.tmpdir, self.files_map
        )
        self.assertIn('CONVENTIONS.yaml', yamls)
        self.assertIn('TESTING.yaml', yamls)
        self.assertIn('ERRORS.yaml', yamls)
        self.assertIn('GIT_WORKFLOW.yaml', yamls)


class TestTemplates(unittest.TestCase):
    """Tests para templates de proyectos"""
    
    def test_suggest_template(self):
        """Sugiere template correcto segun stack"""
        # Python + Flask
        template = suggest_template(['Python'], {'backend': ['Flask'], 'frontend': [], 'db': [], 'other': []})
        self.assertEqual(template, 'python_flask')
        
        # Vue frontend
        template = suggest_template(['JavaScript'], {'backend': [], 'frontend': ['Vue 3'], 'db': [], 'other': []})
        self.assertEqual(template, 'vue')


class TestInstallFlow(unittest.TestCase):
    """Tests de integración para el flujo de instalación completo"""
    
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        # Crear un proyecto de prueba con archivos
        with open(os.path.join(self.tmpdir, 'app.py'), 'w') as f:
            f.write('"""Flask app"""\nfrom flask import Flask\n\napp = Flask(__name__)\n\n@app.route("/")\ndef index():\n    return "hello"\n')
        with open(os.path.join(self.tmpdir, 'requirements.txt'), 'w') as f:
            f.write('flask==3.0\n')
    
    def tearDown(self):
        shutil.rmtree(self.tmpdir)
    
    def test_full_install(self):
        """Ejecuta instalación completa y verifica resultados"""
        from main import install
        success = install(self.tmpdir, auto_mode=True)
        self.assertTrue(success)
        
        # Verificar que .ai/ existe con todos los archivos
        ai_dir = os.path.join(self.tmpdir, '.ai')
        self.assertTrue(os.path.isdir(ai_dir))
        
        expected_files = [
            'PROJECT_INDEX.yaml', 'ARCHITECTURE.yaml', 'FLOW.yaml',
            'GRAPH.yaml', 'CONVENTIONS.yaml', 'TESTING.yaml',
            'ERRORS.yaml', 'GIT_WORKFLOW.yaml',
            'CHANGES.yaml', 'SUMMARIES.yaml', 'CONTEXT_BUDGET.yaml', 'PROTOCOL.yaml',
            'update.py', 'update_index.py', 'pre-commit.hook'
        ]
        for fname in expected_files:
            self.assertTrue(
                os.path.exists(os.path.join(ai_dir, fname)),
                f"Falta {fname} en .ai/"
            )
        
        # Verificar que AGENT_GUIDE.md existe
        self.assertTrue(os.path.exists(os.path.join(self.tmpdir, 'AGENT_GUIDE.md')))
        
        # Verificar que .ai/src/ (motor) fue copiado
        self.assertTrue(os.path.isdir(os.path.join(ai_dir, 'src')))


if __name__ == '__main__':
    unittest.main()
