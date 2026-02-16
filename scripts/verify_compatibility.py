#!/usr/bin/env python3
"""
Script de verificación de compatibilidad cross-platform
Verifica que todos los archivos usen rutas correctas
"""

import os
import sys
from pathlib import Path


def check_file_for_hardcoded_paths(filepath):
    """Busca rutas hardcoded que puedan causar problemas"""
    issues = []
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines, 1):
        # Buscar barras Windows hardcoded
        if '\\\\' in line and 'Users\\simon' not in line:  # Excluir ejemplos de documentación
            if not line.strip().startswith('#'):  # Excluir comentarios
                issues.append(f"Línea {i}: Posible barra Windows hardcoded: {line.strip()[:60]}")
        
        # Buscar rutas absolutas sospechosas (excepto en documentación)
        if filepath.endswith('.py'):
            if 'C:' in line or 'D:' in line:
                if not line.strip().startswith('#'):
                    issues.append(f"Línea {i}: Posible ruta absoluta Windows: {line.strip()[:60]}")
            if line.strip().startswith('/home/') or line.strip().startswith('/usr/'):
                issues.append(f"Línea {i}: Posible ruta absoluta Linux: {line.strip()[:60]}")
    
    return issues


def verify_python_files():
    """Verifica archivos Python principales"""
    print("🔍 Verificando compatibilidad cross-platform...\n")
    
    python_files = [
        'install_online.py',
        'install.py',
        'scripts/configure_online_installer.py',
        'src/main.py',
        'src/core/scanner.py',
        'src/core/validators.py',
        'src/core/detectors.py',
        'src/core/extractors.py',
    ]
    
    all_ok = True
    
    for pyfile in python_files:
        if not os.path.exists(pyfile):
            print(f"⚠️  {pyfile}: No encontrado")
            continue
        
        issues = check_file_for_hardcoded_paths(pyfile)
        
        if issues:
            print(f"❌ {pyfile}:")
            for issue in issues:
                print(f"   {issue}")
            all_ok = False
        else:
            print(f"✅ {pyfile}: OK")
    
    return all_ok


def verify_os_path_usage():
    """Verifica que se use os.path.join en lugar de concatenación de strings"""
    print("\n🔍 Verificando uso de os.path.join()...\n")
    
    # Archivos críticos
    critical_files = [
        'install_online.py',
        'scripts/configure_online_installer.py',
    ]
    
    for filepath in critical_files:
        if not os.path.exists(filepath):
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        has_join = 'os.path.join' in content
        has_pathlib = 'from pathlib import Path' in content
        
        if has_join or has_pathlib:
            print(f"✅ {filepath}: Usa rutas cross-platform")
        else:
            print(f"⚠️  {filepath}: Verifica el uso de rutas")


def verify_scripts():
    """Verifica que existan scripts para todas las plataformas"""
    print("\n🔍 Verificando scripts multiplataforma...\n")
    
    scripts = {
        'Windows PowerShell': 'scripts/git_push.ps1',
        'Windows CMD': 'scripts/git_push.bat',
        'Linux/macOS Bash': 'scripts/git_push.sh',
    }
    
    all_ok = True
    for platform, script_path in scripts.items():
        if os.path.exists(script_path):
            print(f"✅ {platform}: {script_path}")
        else:
            print(f"❌ {platform}: {script_path} no encontrado")
            all_ok = False
    
    return all_ok


def verify_structure():
    """Verifica estructura de carpetas"""
    print("\n🔍 Verificando estructura del proyecto...\n")
    
    required_dirs = {
        'src': 'Código fuente',
        'docs': 'Documentación',
        'scripts': 'Scripts de ayuda',
        'tests': 'Tests unitarios',
    }
    
    all_ok = True
    for dir_name, description in required_dirs.items():
        if os.path.isdir(dir_name):
            print(f"✅ {dir_name}/ - {description}")
        else:
            print(f"❌ {dir_name}/ - {description} (no encontrado)")
            all_ok = False
    
    return all_ok


def main():
    print("\n" + "=" * 70)
    print("  VERIFICACIÓN DE COMPATIBILIDAD CROSS-PLATFORM")
    print("  AI Agent Wizard v1.1.0")
    print("=" * 70 + "\n")
    
    # Verificar que estamos en la raíz del proyecto
    if not os.path.exists('install_online.py'):
        print("❌ ERROR: Ejecuta este script desde la raíz del proyecto")
        print("   Uso: python scripts/verify_compatibility.py\n")
        sys.exit(1)
    
    checks = [
        verify_structure(),
        verify_python_files(),
        verify_scripts(),
    ]
    
    verify_os_path_usage()
    
    print("\n" + "=" * 70)
    if all(checks):
        print("✅ VERIFICACIÓN COMPLETADA - Todo OK")
        print("   El proyecto es compatible con Windows, Linux y macOS")
    else:
        print("⚠️  VERIFICACIÓN COMPLETADA - Revisar advertencias")
        print("   Algunos archivos pueden necesitar ajustes")
    print("=" * 70 + "\n")
    
    return 0 if all(checks) else 1


if __name__ == '__main__':
    sys.exit(main())
