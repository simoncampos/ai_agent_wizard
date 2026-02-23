"""
Detectores de stack tecnologico (lenguajes, frameworks, servicios).
Analiza el proyecto para identificar tecnologias usadas.
"""

import os
import json
import subprocess
from pathlib import Path

try:
    from utils.warnings import warn, vprint
except ImportError:
    def warn(msg, ctx=""): pass
    def vprint(msg, level=1): pass


def detect_languages(project_path, source_files_iter):
    """
    Detecta lenguajes usados por extension de archivo.
    
    Args:
        project_path: Ruta del proyecto
        source_files_iter: Iterador de archivos fuente
        
    Returns:
        Lista ordenada de lenguajes detectados
    """
    vprint("Detectando lenguajes...", level=1)
    
    lang_map = {
        '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
        '.tsx': 'TypeScript (React)', '.jsx': 'JavaScript (React)',
        '.vue': 'Vue', '.svelte': 'Svelte',
        '.java': 'Java', '.kt': 'Kotlin', '.go': 'Go',
        '.rs': 'Rust', '.rb': 'Ruby', '.php': 'PHP',
        '.cs': 'C#', '.c': 'C', '.cpp': 'C++',
        '.html': 'HTML', '.css': 'CSS', '.scss': 'SCSS',
    }
    
    found = set()
    for filepath in source_files_iter:
        ext = Path(filepath).suffix.lower()
        if ext in lang_map:
            lang = lang_map[ext]
            found.add(lang)
            vprint(f"Detectado {lang}", level=2)
    
    vprint(f"Total lenguajes: {len(found)}", level=1)
    return sorted(found)


def detect_frameworks(project_path):
    """
    Detecta frameworks por archivos de configuracion.
    
    Args:
        project_path: Ruta del proyecto
        
    Returns:
        Dict {'backend': [...], 'frontend': [...], 'db': [...], 'other': [...]}
    """
    vprint("Detectando frameworks...", level=1)
    
    detections = {
        'backend': [],
        'frontend': [],
        'db': [],
        'other': []
    }

    # Indicadores por archivo de configuracion
    indicators = {
        # Backend
        'requirements.txt': ('backend', 'Python (pip)'),
        'Pipfile': ('backend', 'Python (pipenv)'),
        'pyproject.toml': ('backend', 'Python (poetry/modern)'),
        'manage.py': ('backend', 'Django'),
        'app.py': ('backend', 'Flask'),
        'api.py': ('backend', 'Flask/FastAPI'),
        'main.py': ('backend', 'Python App'),
        'go.mod': ('backend', 'Go'),
        'Cargo.toml': ('backend', 'Rust'),
        'pom.xml': ('backend', 'Java (Maven)'),
        'build.gradle': ('backend', 'Java/Kotlin (Gradle)'),
        'Gemfile': ('backend', 'Ruby'),
        'composer.json': ('backend', 'PHP (Composer)'),
        'artisan': ('backend', 'Laravel'),
        'wp-config.php': ('backend', 'WordPress'),
        'symfony.lock': ('backend', 'Symfony'),
        'nest-cli.json': ('backend', 'NestJS'),
        'celery.py': ('backend', 'Celery'),
        # Frontend
        'package.json': ('frontend', 'Node.js'),
        'next.config.js': ('frontend', 'Next.js'),
        'next.config.mjs': ('frontend', 'Next.js'),
        'next.config.ts': ('frontend', 'Next.js'),
        'nuxt.config.ts': ('frontend', 'Nuxt'),
        'nuxt.config.js': ('frontend', 'Nuxt'),
        'vite.config.js': ('frontend', 'Vite'),
        'vite.config.ts': ('frontend', 'Vite'),
        'angular.json': ('frontend', 'Angular'),
        'svelte.config.js': ('frontend', 'SvelteKit'),
        'tailwind.config.js': ('frontend', 'Tailwind CSS'),
        'tailwind.config.ts': ('frontend', 'Tailwind CSS'),
        'gatsby-config.js': ('frontend', 'Gatsby'),
        'remix.config.js': ('frontend', 'Remix'),
        # DB
        'prisma': ('db', 'Prisma'),
        'drizzle.config.ts': ('db', 'Drizzle'),
        # Otros
        'docker-compose.yml': ('other', 'Docker Compose'),
        'docker-compose.yaml': ('other', 'Docker Compose'),
        'Dockerfile': ('other', 'Docker'),
        '.github': ('other', 'GitHub Actions'),
        'Makefile': ('other', 'Make'),
        'Procfile': ('other', 'Heroku'),
        'vercel.json': ('other', 'Vercel'),
        'netlify.toml': ('other', 'Netlify'),
    }

    for filename, (category, name) in indicators.items():
        file_path = Path(project_path) / filename
        if file_path.exists():
            if name not in detections[category]:
                detections[category].append(name)
                vprint(f"Detectado {name} ({filename})", level=2)

    # Detectar frameworks especificos en package.json
    pkg_json = Path(project_path) / 'package.json'
    if pkg_json.exists():
        try:
            with open(pkg_json, 'r', encoding='utf-8') as f:
                pkg = json.load(f)
            all_deps = {}
            all_deps.update(pkg.get('dependencies', {}))
            all_deps.update(pkg.get('devDependencies', {}))
            
            fw_deps = {
                'react': 'React', 'vue': 'Vue 3', 'svelte': 'Svelte',
                'express': 'Express', 'fastify': 'Fastify', 'koa': 'Koa',
                'next': 'Next.js', 'nuxt': 'Nuxt',
                '@angular/core': 'Angular',
                '@nestjs/core': 'NestJS',
                'hapi': 'Hapi',
                'socket.io': 'Socket.IO',
                'graphql': 'GraphQL',
                '@apollo/server': 'Apollo GraphQL',
                'prisma': 'Prisma',
                'sequelize': 'Sequelize',
                'mongoose': 'Mongoose',
                'typeorm': 'TypeORM',
                'tailwindcss': 'Tailwind CSS',
            }
            for dep, name in fw_deps.items():
                if dep in all_deps:
                    cat = 'frontend' if dep in ['react', 'vue', 'svelte', '@angular/core', 'tailwindcss'] else 'backend'
                    if dep in ['prisma', 'sequelize', 'mongoose', 'typeorm']:
                        cat = 'db'
                    if name not in detections[cat]:
                        detections[cat].append(name)
                        vprint(f"Detectado {name} (package.json)", level=2)
                        
        except (json.JSONDecodeError, IOError) as e:
            warn(f"Error parseando package.json: {e}", "detect_frameworks")

    # Detectar Flask/FastAPI/Django en requirements.txt
    req_files = ['requirements.txt', 'Pipfile', 'pyproject.toml']
    for req_file in req_files:
        req_path = Path(project_path) / req_file
        if req_path.exists():
            try:
                content = req_path.read_text(encoding='utf-8').lower()
                if 'flask' in content and 'Flask' not in detections['backend']:
                    detections['backend'].append('Flask')
                    vprint(f"Detectado Flask ({req_file})", level=2)
                if 'fastapi' in content and 'FastAPI' not in detections['backend']:
                    detections['backend'].append('FastAPI')
                    vprint(f"Detectado FastAPI ({req_file})", level=2)
                if 'django' in content and 'Django' not in detections['backend']:
                    detections['backend'].append('Django')
                    vprint(f"Detectado Django ({req_file})", level=2)
                if 'djangorestframework' in content and 'DRF' not in detections['backend']:
                    detections['backend'].append('DRF')
                    vprint(f"Detectado Django REST Framework ({req_file})", level=2)
                if 'celery' in content and 'Celery' not in detections['backend']:
                    detections['backend'].append('Celery')
                    vprint(f"Detectado Celery ({req_file})", level=2)
                if 'sqlalchemy' in content and 'SQLAlchemy' not in detections['db']:
                    detections['db'].append('SQLAlchemy')
                    vprint(f"Detectado SQLAlchemy ({req_file})", level=2)
                if 'pydantic' in content and 'Pydantic' not in detections['backend']:
                    detections['backend'].append('Pydantic')
                    vprint(f"Detectado Pydantic ({req_file})", level=2)
                if 'pytest' in content and 'pytest' not in detections['other']:
                    detections['other'].append('pytest')
                    vprint(f"Detectado pytest ({req_file})", level=2)
            except IOError as e:
                warn(f"No se pudo leer {req_file}: {e}", "detect_frameworks")

    # Detectar frameworks PHP en composer.json
    composer_json = Path(project_path) / 'composer.json'
    if composer_json.exists():
        try:
            with open(composer_json, 'r', encoding='utf-8') as f:
                composer = json.load(f)
            all_deps = {}
            all_deps.update(composer.get('require', {}))
            all_deps.update(composer.get('require-dev', {}))
            
            php_fw = {
                'laravel/framework': 'Laravel',
                'symfony/symfony': 'Symfony',
                'symfony/framework-bundle': 'Symfony',
                'slim/slim': 'Slim',
                'cakephp/cakephp': 'CakePHP',
                'yiisoft/yii2': 'Yii2',
            }
            for dep, name in php_fw.items():
                if dep in all_deps and name not in detections['backend']:
                    detections['backend'].append(name)
                    vprint(f"Detectado {name} (composer.json)", level=2)
        except (json.JSONDecodeError, IOError) as e:
            warn(f"Error parseando composer.json: {e}", "detect_frameworks")

    vprint(f"Frameworks detectados: backend={len(detections['backend'])}, frontend={len(detections['frontend'])}", level=1)
    return detections


def detect_services(project_path):
    """
    Detecta servicios systemd activos relacionados con el proyecto.
    
    Args:
        project_path: Ruta del proyecto
        
    Returns:
        Lista de diccionarios con info de servicios
    """
    vprint("Detectando servicios systemd...", level=1)
    
    services = []
    try:
        result = subprocess.run(
            ['systemctl', 'list-units', '--type=service', '--state=running', '--no-pager', '--plain'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            project_name = Path(project_path).name.lower().replace('_', '-')
            for line in result.stdout.split('\n'):
                if project_name in line.lower() or 'monitor' in line.lower():
                    parts = line.strip().split()
                    if parts:
                        service_name = parts[0].replace('.service', '')
                        services.append({'name': service_name, 'type': 'systemd'})
                        vprint(f"Servicio detectado: {service_name}", level=2)
                        
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        vprint(f"No se pudieron detectar servicios: {e}", level=2)
    
    return services


def detect_monorepo(project_path):
    """
    Detecta si es un monorepo y retorna workspaces.
    
    Args:
        project_path: Ruta del proyecto
        
    Returns:
        Dict {'is_monorepo': bool, 'tool': str, 'workspaces': []}
    """
    vprint("Verificando si es monorepo...", level=1)
    
    monorepo_indicators = {
        'lerna.json': 'Lerna',
        'pnpm-workspace.yaml': 'pnpm',
        'nx.json': 'Nx',
        'rush.json': 'Rush',
    }
    
    for indicator, tool in monorepo_indicators.items():
        indicator_path = Path(project_path) / indicator
        if indicator_path.exists():
            workspaces = []
            
            if indicator == 'lerna.json':
                try:
                    with open(indicator_path) as f:
                        config = json.load(f)
                        workspaces = config.get('packages', [])
                except:
                    pass
            
            vprint(f"Monorepo detectado: {tool}", level=2)
            return {
                'is_monorepo': True,
                'tool': tool,
                'workspaces': workspaces
            }
    
    # Detectar por package.json con workspaces
    pkg_path = Path(project_path) / 'package.json'
    if pkg_path.exists():
        try:
            with open(pkg_path) as f:
                pkg = json.load(f)
                if 'workspaces' in pkg:
                    vprint("Monorepo detectado: npm/yarn workspaces", level=2)
                    return {
                        'is_monorepo': True,
                        'tool': 'npm/yarn workspaces',
                        'workspaces': pkg['workspaces']
                    }
        except:
            pass
    
    vprint("No es un monorepo", level=2)
    return {'is_monorepo': False}
