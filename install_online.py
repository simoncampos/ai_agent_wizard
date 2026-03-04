#!/usr/bin/env python3
"""
AI Agent Wizard - Instalador Online
Descarga la última versión desde GitHub, instala y limpia automáticamente.

USO:
    python install_online.py [opciones]
    
OPCIONES:
    --auto          Modo no interactivo
    --verbose, -v   Mostrar progreso detallado
    --help, -h      Mostrar esta ayuda

CARACTERÍSTICAS:
    ok Descarga código actualizado desde GitHub
    ok Instala sobre proyecto actual
    ok Limpia archivos temporales automáticamente
    ok Sin dependencias externas (solo Python stdlib)
"""

import sys
import os
import shutil
import tempfile
import urllib.request
import zipfile
import ssl
from pathlib import Path


# ============================================================================
# CONFIGURACIÓN
# ============================================================================
GITHUB_REPO = "simoncampos/ai_agent_wizard"
GITHUB_BRANCH = "main"


def print_banner():
    """Muestra banner de presentación"""
    print("\n" + "=" * 70)
    print("  AI AGENT WIZARD - INSTALADOR v5.0.0")
    print("  Indexación inteligente: menos tokens, cero navegación")
    print("=" * 70 + "\n")


def download_repository(repo_url, dest_dir, verbose=False):
    """Descarga repositorio de GitHub como ZIP"""
    # Construir URL del ZIP
    zip_url = f"https://github.com/{repo_url}/archive/refs/heads/{GITHUB_BRANCH}.zip"
    zip_path = os.path.join(dest_dir, "ai_agent_wizard.zip")
    
    if verbose:
        print(f"   Descargando desde: {zip_url}")
    else:
        print("   Descargando código actualizado...", end="", flush=True)
    
    try:
        # Crear contexto SSL sin verificación (para evitar errores de certificado)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Descargar con progreso
        def report_progress(block_num, block_size, total_size):
            if verbose and total_size > 0:
                percent = int(100 * block_num * block_size / total_size)
                print(f"\r     Progreso: {percent}%", end="", flush=True)
        
        # Instalar opener con contexto SSL
        opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
        urllib.request.install_opener(opener)
        
        urllib.request.urlretrieve(zip_url, zip_path, report_progress if verbose else None)
        
        if verbose:
            print()
        else:
            print(" ok")
        
        return zip_path
        
    except Exception as e:
        print(f" FAIL\n  ERROR: No se pudo descargar el repositorio: {e}")
        return None


def extract_repository(zip_path, dest_dir, verbose=False):
    """Extrae el ZIP descargado"""
    if verbose:
        print(f"   Extrayendo archivos...")
    else:
        print("   Extrayendo archivos...", end="", flush=True)
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(dest_dir)
        
        if not verbose:
            print(" ok")
        
        # Buscar directorio extraído (GitHub crea carpeta con nombre-branch)
        extracted_dirs = [d for d in os.listdir(dest_dir) if os.path.isdir(os.path.join(dest_dir, d))]
        if not extracted_dirs:
            raise Exception("No se encontró directorio extraído")
        
        extracted_path = os.path.join(dest_dir, extracted_dirs[0])
        
        if verbose:
            print(f"     Extraído en: {extracted_path}")
        
        return extracted_path
        
    except Exception as e:
        print(f" FAIL\n  ERROR: No se pudo extraer el archivo: {e}")
        return None


def install_wizard(extracted_path, project_path, auto_mode=False, verbose=False):
    """Instala el wizard usando el código descargado"""
    print("\n   Iniciando instalación...\n")
    
    # Verificar que exista src/ en el código descargado
    src_path = os.path.join(extracted_path, 'src')
    if not os.path.exists(src_path):
        print(f"  ERROR: No se encontró carpeta 'src' en el código descargado")
        return False
    
    # Agregar src al path para importar
    sys.path.insert(0, src_path)
    
    try:
        # Importar y ejecutar el instalador
        from main import install
        
        success = install(
            project_path=project_path,
            auto_mode=auto_mode,
            verbose=verbose
        )
        
        return success
        
    except ImportError as e:
        print(f"  ERROR: No se pudo importar el instalador: {e}")
        return False
    except Exception as e:
        print(f"  ERROR durante la instalación: {e}")
        return False


def cleanup(temp_dir, verbose=False):
    """Limpia archivos temporales"""
    if verbose:
        print(f"\n   Limpiando archivos temporales: {temp_dir}")
    else:
        print("\n   Limpiando archivos temporales...", end="", flush=True)
    
    try:
        shutil.rmtree(temp_dir, ignore_errors=True)
        if not verbose:
            print(" ok")
    except Exception as e:
        if verbose:
            print(f"     Advertencia: No se pudo limpiar completamente: {e}")


def main():
    """Entry point principal"""
    print_banner()
    
    # Parsear argumentos
    auto_mode = '--auto' in sys.argv
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    
    if '--help' in sys.argv or '-h' in sys.argv:
        print(__doc__)
        sys.exit(0)
    
    # Obtener proyecto actual
    args = [a for a in sys.argv[1:] if not a.startswith('--') and not a.startswith('-')]
    project_path = os.path.abspath(args[0] if args else os.getcwd())
    project_name = os.path.basename(project_path)
    
    print(f"   Proyecto: {project_name}")
    print(f"   Ruta: {project_path}\n")
    
    # Confirmar instalación (si no es auto)
    if not auto_mode:
        print(f"\n  Se descargará desde: github.com/{GITHUB_REPO}")
        response = input("  ¿Continuar? [S/n]: ").strip().lower()
        if response and response not in ['s', 'si', 'sí', 'y', 'yes']:
            print("\n  Instalación cancelada.\n")
            sys.exit(0)
        print()
    
    # Crear directorio temporal
    temp_dir = tempfile.mkdtemp(prefix='ai_agent_wizard_')
    
    if verbose:
        print(f"   Directorio temporal: {temp_dir}\n")
    
    try:
        # Fase 1: Descargar
        zip_path = download_repository(GITHUB_REPO, temp_dir, verbose)
        if not zip_path:
            cleanup(temp_dir, verbose)
            sys.exit(1)
        
        # Fase 2: Extraer
        extracted_path = extract_repository(zip_path, temp_dir, verbose)
        if not extracted_path:
            cleanup(temp_dir, verbose)
            sys.exit(1)
        
        # Fase 3: Instalar
        success = install_wizard(extracted_path, project_path, auto_mode, verbose)
        
        # Fase 4: Limpiar
        cleanup(temp_dir, verbose)
        
        # Resultado final
        if success:
            print("\n  " + "=" * 70)
            print("  ✅ INSTALACIÓN ONLINE COMPLETADA")
            print("  " + "=" * 70)
            print(f"\n  El sistema .ai/ está listo en: {project_path}")
            print(f"  Próximo paso: Lee .ai/FLOW.yaml para usar el sistema\n")
        else:
            print("\n  ❌ La instalación no se completó correctamente.\n")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n  ⚠️  Instalación interrumpida por el usuario.")
        cleanup(temp_dir, verbose)
        sys.exit(1)
    except Exception as e:
        print(f"\n  ERROR INESPERADO: {e}")
        cleanup(temp_dir, verbose)
        sys.exit(1)


if __name__ == '__main__':
    main()
