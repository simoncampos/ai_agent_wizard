"""
Validadores de entorno y requisitos del sistema.
Verifica Python 3.7+, Git, permisos de escritura, etc.
"""

import sys
import os
import shutil
import subprocess


def check_python_version():
    """Valida Python 3.7+"""
    if sys.version_info < (3, 7):
        return False, f"Python 3.7+ requerido (actual: {sys.version_info.major}.{sys.version_info.minor})"
    return True, f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def check_git_installed():
    """Valida que Git este disponible"""
    try:
        result = subprocess.run(
            ['git', '--version'],
            capture_output=True,
            timeout=3,
            text=True
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            return True, version
        return False, "Git no responde correctamente"
    except FileNotFoundError:
        return False, "Git no esta instalado"
    except subprocess.TimeoutExpired:
        return False, "Git no responde (timeout)"


def check_write_permissions(path):
    """Valida permisos de escritura en el directorio"""
    test_file = os.path.join(path, '.write_test_tmp')
    try:
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        return True, "Permisos OK"
    except (IOError, PermissionError) as e:
        return False, f"Sin permisos de escritura: {e}"


def check_disk_space(path, min_mb=10):
    """Verifica que haya espacio en disco suficiente (multiplataforma)"""
    try:
        usage = shutil.disk_usage(path)
        free_mb = usage.free / (1024 * 1024)
        if free_mb < min_mb:
            return False, f"Espacio insuficiente: {free_mb:.1f}MB (minimo: {min_mb}MB)"
        return True, f"{free_mb:.1f}MB disponibles"
    except Exception:
        return True, "No se pudo verificar (asumiendo OK)"


def validate_environment(project_path):
    """Ejecuta todas las validaciones y retorna report"""
    checks = {
        'Python 3.7+': check_python_version(),
        'Git instalado': check_git_installed(),
        'Permisos de escritura': check_write_permissions(project_path),
        'Espacio en disco': check_disk_space(project_path),
    }
    
    all_ok = all(result[0] for result in checks.values())
    return all_ok, checks


def validate_project_path(project_path):
    """Valida que la ruta del proyecto sea valida"""
    if not os.path.exists(project_path):
        return False, f"El directorio '{project_path}' no existe"
    
    if not os.path.isdir(project_path):
        return False, f"'{project_path}' no es un directorio"
    
    return True, "Directorio valido"
