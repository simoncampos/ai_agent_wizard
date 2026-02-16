"""Core modules - Escaneo, detección y extracción"""

from .scanner import scan_files, is_empty_project, iter_source_files
from .detectors import detect_languages, detect_frameworks, detect_services, detect_monorepo  
from .extractors import extract_functions, extract_endpoints, extract_vue_components, extract_dependencies
from .validators import validate_environment, check_python_version, check_git_installed

__all__ = [
    'scan_files',
    'is_empty_project',
    'iter_source_files',
    'detect_languages',
    'detect_frameworks',
    'detect_services',
    'detect_monorepo',
    'extract_functions',
    'extract_endpoints',
    'extract_vue_components',
    'extract_dependencies',
    'validate_environment',
    'check_python_version',
    'check_git_installed',
]
