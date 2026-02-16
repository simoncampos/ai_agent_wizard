#!/usr/bin/env python3
"""
Script para actualizar la configuración del instalador online
Uso: python scripts/configure_online_installer.py <github_repo> [branch]

Ejemplo:
    python scripts/configure_online_installer.py simoncampos/ai-agent-wizard
    python scripts/configure_online_installer.py simoncampos/ai-agent-wizard develop
"""

import sys
import os
import re


def update_installer_config(repo, branch="main"):
    """
    Actualiza la configuración del instalador online
    
    Args:
        repo: Repositorio en formato "owner/repo"
        branch: Rama a usar (default: main)
    """
    # Buscar install_online.py en el directorio raíz del proyecto (padre de scripts/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    installer_path = os.path.join(project_root, 'install_online.py')
    
    if not os.path.exists(installer_path):
        print(f"❌ Error: No se encontró {installer_path}")
        return False
    
    # Leer contenido actual
    with open(installer_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazar GITHUB_REPO
    content = re.sub(
        r'GITHUB_REPO\s*=\s*["\'][^"\']*["\']',
        f'GITHUB_REPO = "{repo}"',
        content
    )
    
    # Reemplazar GITHUB_BRANCH
    content = re.sub(
        r'GITHUB_BRANCH\s*=\s*["\'][^"\']*["\']',
        f'GITHUB_BRANCH = "{branch}"',
        content
    )
    
    # Guardar cambios
    with open(installer_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Configuración actualizada:")
    print(f"   Repositorio: {repo}")
    print(f"   Rama: {branch}")
    print(f"   Archivo: {installer_path}")
    
    # Mostrar URL de descarga
    raw_url = f"https://raw.githubusercontent.com/{repo}/{branch}/install_online.py"
    print(f"\n📥 URL de descarga para usuarios:")
    print(f"   {raw_url}")
    
    print(f"\n💡 Comando para usuarios:")
    print(f"   curl -O {raw_url} && python3 install_online.py --auto")
    
    return True


def validate_repo_format(repo):
    """Valida que el repo esté en formato correcto"""
    pattern = r'^[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+$'
    if not re.match(pattern, repo):
        print(f"❌ Error: Formato inválido '{repo}'")
        print("   Debe ser: owner/repo (ejemplo: usuario/ai-agent-wizard)")
        return False
    return True


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    repo = sys.argv[1]
    branch = sys.argv[2] if len(sys.argv) > 2 else "main"
    
    if not validate_repo_format(repo):
        sys.exit(1)
    
    if update_installer_config(repo, branch):
        print("\n✅ Listo para distribuir install_online.py")
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
