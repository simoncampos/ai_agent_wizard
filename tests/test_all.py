"""
Tests unitarios del AI Agent Wizard
"""

import unittest
import tempfile
import os
import shutil
import sys

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.validators import check_python_version, check_git_installed
from core.scanner import scan_files, is_empty_project
from core.detectors import detect_languages
from core.extractors import extract_functions
from templates.project_templates import suggest_template


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


class TestExtractors(unittest.TestCase):
    """Tests para extractores"""
    
    def test_extract_functions(self):
        """Extrae funciones de Python"""
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


if __name__ == '__main__':
    unittest.main()
