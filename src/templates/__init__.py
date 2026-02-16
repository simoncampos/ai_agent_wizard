"""Templates modules - Templates de proyectos y contenido"""

from .project_templates import (
    PROJECT_TEMPLATES,
    get_template,
    list_templates,
    suggest_template,
    create_structure
)

__all__ = [
    'PROJECT_TEMPLATES',
    'get_template',
    'list_templates',
    'suggest_template',
    'create_structure',
]
