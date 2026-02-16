"""
Escaner de archivos del proyecto.
Itera y mapea todos los archivos fuente excluyendo dependencias.
Construye el índice base para acceso directo sin navegación manual.
"""

import os
import sys
from pathlib import Path

# Import condicional para warnings
try:
    from utils.warnings import warn, vprint
except ImportError:
    # Fallback si no se puede importar
    def warn(msg, ctx=""): pass
    def vprint(msg, level=1): pass

# Directorios a excluir del escaneo
EXCLUDE_DIRS = {
    'node_modules', '.venv', 'venv', 'env', '__pycache__', '.git',
    'dist', 'build', '.next', '.nuxt', '.output', '.cache',
    'coverage', '.tox', '.mypy_cache', '.pytest_cache',
    'vendor', 'target', 'bin', 'obj', '.idea', '.vscode',
}

# Archivos a exclu del escaneo
EXCLUDE_FILES = {
    '.DS_Store', 'Thumbs.db', 'package-lock.json', 'yarn.lock',
    'pnpm-lock.yaml', 'poetry.lock', 'Pipfile.lock',
    'composer.lock', 'Gemfile.lock', 'Cargo.lock'
}

# Extensiones de archivos fuente soportadas
SOURCE_EXTENSIONS = {
    '.py', '.js', '.ts', '.tsx', '.jsx', '.vue', '.svelte',
    '.java', '.kt', '.go', '.rs', '.rb', '.php',
    '.c', '.cpp', '.h', '.hpp', '.cs',
    '.html', '.css', '.scss', '.sass', '.less',
    '.json', '.yaml', '.yml', '.toml', '.xml',
    '.sql', '.sh', '.bash', '.zsh',
    '.md', '.rst', '.txt'
}


def iter_source_files(project_path):
    """
    Itera todos los archivos fuente excluyendo dependencias.
    
    Args:
        project_path: Ruta absoluta del proyecto
        
    Yields:
        Rutas absolutas de archivos fuente
    """
    for root, dirs, files in os.walk(project_path):
        # Filtrar directorios excluidos
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        
        for f in files:
            if f in EXCLUDE_FILES:
                continue
            if Path(f).suffix.lower() in SOURCE_EXTENSIONS:
                yield os.path.join(root, f)


def scan_files(project_path, show_progress=False):
    """
    Escanea archivos y retorna mapa con metadata.
    
    Args:
        project_path: Ruta absoluta del proyecto
        show_progress: Si True, muestra progreso de escaneo
        
    Returns:
        Dict {filepath_relativo: {'type': 'py', 'lines': N, 'content': [lineas]}}
    """
    vprint("Iniciando escaneo de archivos...", level=1)
    
    files_map = {}
    all_files = list(iter_source_files(project_path))
    total = len(all_files)
    
    vprint(f"Total de archivos a escanear: {total}", level=1)
    
    for i, filepath in enumerate(all_files, 1):
        if show_progress and (i % 10 == 0 or i == total):
            percent = int(100 * i / total)
            print(f"\r         Escaneando... {i}/{total} ({percent}%)", end="", flush=True)
        
        rel_path = os.path.relpath(filepath, project_path)
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            ext = Path(filepath).suffix.lstrip('.')
            files_map[rel_path] = {
                'type': ext,
                'lines': len(lines),
                'content': lines
            }
            
            vprint(f"Archivo escaneado: {rel_path} ({len(lines)} lineas)", level=2)
            
        except (IOError, UnicodeDecodeError) as e:
            warn(f"No se pudo leer {rel_path}: {e}", "scan_files")
    
    if show_progress:
        print()  # Nueva linea al terminar
    
    vprint(f"Escaneo completado: {len(files_map)} archivos", level=1)
    return files_map


def is_empty_project(project_path):
    """Verifica si el directorio esta vacio o solo tiene archivos ocultos/git"""
    for item in os.listdir(project_path):
        if item.startswith('.'):
            continue
        return False
    return True


def count_lines_of_code(files_map):
    """Cuenta lineas totales de codigo en el proyecto"""
    return sum(info['lines'] for info in files_map.values())
