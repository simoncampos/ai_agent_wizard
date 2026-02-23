#!/usr/bin/env python3
"""
AI Agent Wizard - Actualizador del Core (.ai/)
Descarga y actualiza el core del sistema (.ai/src/, scripts, hooks)
Luego regenera automáticamente todos los índices.

USO:
    python .ai/update.py [opciones]

OPCIONES:
    --auto          Modo no interactivo
    --verbose, -v   Progreso detallado
    --help, -h      Mostrar esta ayuda

CARACTERÍSTICAS:
    ✓ Descarga última versión del core desde GitHub
    ✓ Actualiza .ai/src/ (motor de indexación)
    ✓ Actualiza scripts (update.py, update_index.py, pre-commit.hook)
    ✓ Regenera automáticamente todos los índices después de actualizar
    ✓ Reinstala git hook automáticamente
"""

import os
import sys
import shutil
import tempfile
import urllib.request
import zipfile
import ssl
from pathlib import Path
import subprocess


# ============================================================================
# CONFIGURACIÓN
# ============================================================================

GITHUB_REPO = "simoncampos/ai_agent_wizard"
GITHUB_BRANCH = "main"


def print_banner():
    """Muestra banner de presentación"""
    print("\n" + "=" * 70)
    print("  AI AGENT WIZARD - ACTUALIZADOR DEL CORE v3.0.0")
    print("  Actualiza sistema .ai/ y regenera índices automáticamente")
    print("=" * 70 + "\n")


def download_repository(verbose=False):
    """Descarga repositorio de GitHub como ZIP"""
    zip_url = f"https://github.com/{GITHUB_REPO}/archive/refs/heads/{GITHUB_BRANCH}.zip"
    temp_dir = tempfile.mkdtemp(prefix='ai_agent_wizard_update_')
    zip_path = os.path.join(temp_dir, "ai_agent_wizard.zip")
    
    if verbose:
        print(f"  📥 Descargando desde: {zip_url}")
    else:
        print("  📥 Descargando última versión del core...", end="", flush=True)
    
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        def report_progress(block_num, block_size, total_size):
            if verbose and total_size > 0:
                percent = int(100 * block_num * block_size / total_size)
                print(f"\r     Progreso: {percent}%", end="", flush=True)
        
        opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
        urllib.request.install_opener(opener)
        
        urllib.request.urlretrieve(zip_url, zip_path, report_progress if verbose else None)
        
        if verbose:
            print()
        else:
            print(" ✓")
        
        return temp_dir, zip_path
        
    except Exception as e:
        print(f" ✗\n  ERROR: No se pudo descargar: {e}")
        return None, None


def extract_repository(zip_path, dest_dir, verbose=False):
    """Extrae el ZIP descargado"""
    if verbose:
        print(f"  📦 Extrayendo archivos...")
    else:
        print("  📦 Extrayendo archivos...", end="", flush=True)
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(dest_dir)
        
        extracted_dirs = [d for d in os.listdir(dest_dir) if os.path.isdir(os.path.join(dest_dir, d))]
        if not extracted_dirs:
            raise Exception("No se encontró directorio extraído")
        
        extracted_path = os.path.join(dest_dir, extracted_dirs[0])
        
        if not verbose:
            print(" ✓")
        
        return extracted_path
        
    except Exception as e:
        print(f" ✗\n  ERROR: No se pudo extraer: {e}")
        return None


def update_core(extracted_path, ai_dir, verbose=False):
    """Actualiza el core del sistema (.ai/)"""
    print()  # Línea en blanco
    errors = []
    updated = []
    
    # 1. Actualizar motor (.ai/src/)
    if verbose:
        print("  🔧 Actualizando motor de indexación (.ai/src/)...", end="", flush=True)
    else:
        print("  🔧 Actualizando motor...", end="", flush=True)
    
    try:
        src_path = os.path.join(extracted_path, 'src')
        if not os.path.isdir(src_path):
            raise Exception("No se encontró directorio src/")
        
        engine_dst = os.path.join(ai_dir, 'src')
        if os.path.exists(engine_dst):
            shutil.rmtree(engine_dst)
        
        shutil.copytree(src_path, engine_dst, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        print(" ✓")
        updated.append('motor')
    except Exception as e:
        print(f" ✗")
        errors.append(f"Motor: {e}")
    
    # 2. Actualizar scripts
    if verbose:
        print("  📝 Actualizando scripts (.ai/)...", end="", flush=True)
    else:
        print("  📝 Actualizando scripts...", end="", flush=True)
    
    try:
        wizard_ai = os.path.join(extracted_path, '.ai')
        
        for script in ['update.py', 'update_index.py', 'pre-commit.hook']:
            src_script = os.path.join(wizard_ai, script)
            dst_script = os.path.join(ai_dir, script)
            
            if os.path.exists(src_script):
                shutil.copy2(src_script, dst_script)
        
        print(" ✓")
        updated.append('scripts')
    except Exception as e:
        print(f" ✗")
        errors.append(f"Scripts: {e}")
    
    # 3. Reinstalar git hook
    project_path = Path(ai_dir).parent
    if verbose:
        print("  🪝 Reinstalando git hook...", end="", flush=True)
    else:
        print("  🪝 Reinstalando hook...", end="", flush=True)
    
    try:
        git_hooks_dir = project_path / '.git' / 'hooks'
        hook_src = Path(ai_dir) / 'pre-commit.hook'
        
        if git_hooks_dir.is_dir() and hook_src.exists():
            hook_dst = git_hooks_dir / 'pre-commit'
            shutil.copy2(str(hook_src), str(hook_dst))
            
            if os.name != 'nt':
                os.chmod(str(hook_dst), 0o755)
            
            print(" ✓")
            updated.append('hook')
        else:
            print(" ⊘ (no Git)")
    except Exception as e:
        print(f" ⚠")
    
    return errors, updated


def regenerate_indices(ai_dir, verbose=False):
    """Regenera todos los índices automáticamente"""
    print()  # Línea en blanco
    print("  🔄 Regenerando índices (automático)...", end="", flush=True)
    
    try:
        update_script = Path(ai_dir) / 'update_index.py'
        if not update_script.exists():
            raise Exception("No se encontró update_index.py")
        
        args = ['--verbose'] if verbose else ['--quiet']
        result = subprocess.run(
            [sys.executable, str(update_script)] + args,
            cwd=str(Path(ai_dir).parent),
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode != 0:
            raise Exception(result.stderr or "update_index.py falló")
        
        print(" ✓")
        return True
        
    except Exception as e:
        print(f" ✗")
        print(f"  ERROR: {e}")
        return False


def cleanup(temp_dir):
    """Limpia archivos temporales"""
    try:
        shutil.rmtree(temp_dir, ignore_errors=True)
    except Exception:
        pass


def main():
    """Entry point principal"""
    print_banner()
    
    auto_mode = '--auto' in sys.argv
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    
    if '--help' in sys.argv or '-h' in sys.argv:
        print(__doc__)
        sys.exit(0)
    
    # Obtener rutas
    ai_dir = os.path.dirname(os.path.abspath(__file__))
    project_path = os.path.dirname(ai_dir)
    
    print(f"  📂 Proyecto: {os.path.basename(project_path)}")
    print(f"  📍 Core en: {ai_dir}\n")
    
    # Confirmación (si no es auto)
    if not auto_mode:
        print("  ⚠️  Esta operación:")
        print("     1. Descarga la última versión del core desde GitHub")
        print("     2. Actualiza .ai/src/, scripts y git hook")
        print("     3. Regenera automáticamente todos los índices YAML")
        print()
        response = input("  ¿Continuar? [S/n]: ").strip().lower()
        if response and response not in ['s', 'si', 'sí', 'y', 'yes']:
            print("\n  Cancelado.\n")
            sys.exit(0)
    
    # Fase 1: Descargar
    temp_dir, zip_path = download_repository(verbose)
    if not temp_dir:
        sys.exit(1)
    
    try:
        # Fase 2: Extraer
        extracted_path = extract_repository(zip_path, temp_dir, verbose)
        if not extracted_path:
            sys.exit(1)
        
        # Fase 3: Actualizar core
        errors, updated = update_core(extracted_path, ai_dir, verbose)
        
        if errors:
            print()
            for error in errors:
                print(f"  ⚠️  {error}")
        
        # Fase 4: Regenerar índices automáticamente
        success = regenerate_indices(ai_dir, verbose)
        
        # Resultado final
        print()
        print("  " + "=" * 70)
        
        if success:
            print("  ✅ ACTUALIZACIÓN COMPLETADA")
            print("  " + "=" * 70)
            print(f"\n  Actualizado: {', '.join(updated)}")
            print(f"  Índices: regenerados automáticamente")
            print(f"  Versión core: v3.0.0\n")
        else:
            print("  ⚠️  ACTUALIZACIÓN CON ERRORES")
            print("  " + "=" * 70)
            print(f"\n  Actualizado: {', '.join(updated)}")
            print(f"  Índices: NO se regeneraron correctamente")
            print(f"  Ejecuta: python .ai/update_index.py --verbose\n")
            sys.exit(1)
        
    finally:
        cleanup(temp_dir)


if __name__ == '__main__':
    main()
