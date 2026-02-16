# AI_AGENT_WIZARD - Instrucciones para Agentes de IA

## IMPORTANTE: Lee esto antes de hacer cualquier cosa
Este proyecto YA tiene un sistema de índice instalado en `.ai/`.
NO lo creaste tú. NO lo modifiques. NO intentes recrearlo.
Solo ÚSALO para trabajar de forma eficiente.

## Tu primer paso OBLIGATORIO
Antes de leer o modificar cualquier archivo del proyecto, lee estos archivos (ya existen):
1. `.ai/FLOW.yaml` — Te explica cómo usar el sistema de índices
2. `.ai/GRAPH.yaml` — Grafo comprimido de dependencias entre módulos
3. `.ai/PROJECT_INDEX.yaml` — Mapa completo: cada función, endpoint y componente con su archivo y línea exacta

## Reglas de trabajo
- NUNCA leas un archivo completo si solo necesitas una función. Busca su ubicación en PROJECT_INDEX.yaml primero.
- SIEMPRE usa los números de línea del índice para leer solo la sección relevante.
- NUNCA modifiques nada dentro de `.ai/`. Es generado automáticamente.
- Si el usuario modifica código y necesita actualizar índices: `python .ai/update_index.py`

## Qué hay en .ai/ (NO TOCAR)
- `PROJECT_INDEX.yaml` — Funciones, endpoints, componentes con líneas exactas
- `GRAPH.yaml` — Dependencias entre módulos (lectura rápida)
- `ARCHITECTURE.yaml` — Flujo de ejecución y estructura
- `FLOW.yaml` — Instrucciones de uso para ti
- `CONVENTIONS.yaml` — Convenciones de código del proyecto
- `TESTING.yaml` — Cómo ejecutar tests
- `ERRORS.yaml` — Errores conocidos
- `GIT_WORKFLOW.yaml` — Política de commits y ramas
- `update_index.py` — Regenera índices (el usuario lo ejecuta, no tú)
- `update.py` — Actualiza el motor (el usuario lo ejecuta, no tú)
- `src/` — Motor interno de indexación (NUNCA modificar)

Generado por AI Agent Wizard v2.0.0
