"""
Sistema de advertencias y logging para el instalador.
Permite registrar warnings sin detener la ejecucion.
"""

# Sistema global de warnings
WARNINGS = []
VERBOSE = False


def set_verbose(enabled):
    """Activa/desactiva modo verbose"""
    global VERBOSE
    VERBOSE = enabled


def warn(message, context=""):
    """Registra advertencia sin detener ejecucion"""
    warning = f"ADVERTENCIA: {message}"
    if context:
        warning += f" ({context})"
    WARNINGS.append(warning)
    if VERBOSE:
        print(f"  ⚠️  {warning}")


def vprint(message, level=1):
    """Print condicional segun verbosidad"""
    if VERBOSE:
        indent = "  " + "  " * level
        print(f"{indent}🔍 {message}")


def show_warnings_summary():
    """Muestra resumen de advertencias al final"""
    if WARNINGS:
        print(f"\n  {'=' * 60}")
        print(f"  ADVERTENCIAS DURANTE LA INSTALACION ({len(WARNINGS)})")
        print(f"  {'=' * 60}")
        for i, w in enumerate(WARNINGS, 1):
            print(f"  {i}. {w}")


def clear_warnings():
    """Limpia el registro de warnings (util para tests)"""
    global WARNINGS
    WARNINGS = []


def get_warnings():
    """Retorna lista de warnings acumulados"""
    return WARNINGS.copy()
