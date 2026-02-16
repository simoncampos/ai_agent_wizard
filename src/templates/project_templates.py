"""
Templates de estructura de directorios para proyectos nuevos.
Define carpetas tipicas segun el tipo de proyecto detectado.
"""

PROJECT_TEMPLATES = {
    'python': {
        'label': 'Python (general)',
        'dirs': ['src', 'tests', 'docs', 'config'],
    },
    'python_flask': {
        'label': 'Python + Flask (API)',
        'dirs': ['backend', 'backend/routes', 'backend/models', 'backend/Config', 'tests', 'docs'],
    },
    'python_django': {
        'label': 'Python + Django',
        'dirs': ['apps', 'templates', 'static', 'config', 'tests', 'docs'],
    },
    'python_fastapi': {
        'label': 'Python + FastAPI',
        'dirs': ['app', 'app/routers', 'app/models', 'app/schemas', 'tests', 'docs'],
    },
    'node_express': {
        'label': 'Node.js + Express',
        'dirs': ['src', 'src/routes', 'src/controllers', 'src/models', 'src/middleware', 'tests', 'docs'],
    },
    'node_fullstack': {
        'label': 'Node.js Fullstack (frontend + backend)',
        'dirs': ['backend', 'backend/routes', 'backend/models', 'frontend', 'frontend/src',
                 'frontend/src/components', 'frontend/src/styles', 'tests', 'docs'],
    },
    'react': {
        'label': 'React (frontend)',
        'dirs': ['src', 'src/components', 'src/hooks', 'src/styles', 'src/utils', 'public', 'tests'],
    },
    'vue': {
        'label': 'Vue 3 (frontend)',
        'dirs': ['src', 'src/components', 'src/composables', 'src/styles', 'src/utils', 'public', 'tests'],
    },
    'go': {
        'label': 'Go',
        'dirs': ['cmd', 'internal', 'pkg', 'api', 'config', 'docs', 'tests'],
    },
    'rust': {
        'label': 'Rust',
        'dirs': ['src', 'tests', 'docs', 'config'],
    },
    'java': {
        'label': 'Java (Maven/Gradle)',
        'dirs': ['src/main/java', 'src/main/resources', 'src/test/java', 'docs'],
    },
    'generic': {
        'label': 'Generico (estructura minima)',
        'dirs': ['src', 'tests', 'docs', 'config'],
    },
}


def get_template(template_key):
    """Obtiene un template por su clave"""
    return PROJECT_TEMPLATES.get(template_key)


def list_templates():
    """Lista todos los templates disponibles"""
    return [(key, tmpl['label']) for key, tmpl in PROJECT_TEMPLATES.items()]


def suggest_template(languages, frameworks):
    """Sugiere un template basado en el stack detectado"""
    backend = [f.lower() for f in frameworks.get('backend', [])]
    frontend = [f.lower() for f in frameworks.get('frontend', [])]

    # Priorizar por framework detectado
    if any('flask' in f for f in backend):
        return 'python_flask'
    if any('django' in f for f in backend):
        return 'python_django'
    if any('fastapi' in f for f in backend):
        return 'python_fastapi'
    if any('react' in f for f in frontend):
        return 'react'
    if any('vue' in f for f in frontend):
        return 'vue'
    if any('express' in f for f in backend):
        if frontend:
            return 'node_fullstack'
        return 'node_express'

    # Por lenguaje
    if 'Python' in languages:
        return 'python'
    if 'Go' in languages:
        return 'go'
    if 'Rust' in languages:
        return 'rust'
    if 'Java' in languages:
        return 'java'
    if any('JavaScript' in l or 'TypeScript' in l for l in languages):
        return 'node_express'

    return 'generic'


def create_structure(project_path, template_key):
    """Crea la estructura de directorios basada en el template"""
    import os
    
    template = get_template(template_key)
    if not template:
        return []

    created = []
    for dir_path in template['dirs']:
        full_path = os.path.join(project_path, dir_path)
        if not os.path.exists(full_path):
            os.makedirs(full_path, exist_ok=True)
            created.append(dir_path)

    return created
