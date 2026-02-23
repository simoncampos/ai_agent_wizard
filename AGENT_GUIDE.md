# ai_agent_wizard - Instrucciones para Agentes de IA

## IMPORTANTE: Lee esto antes de hacer cualquier cosa
Este proyecto YA tiene un sistema de índice instalado en `.ai/`.
NO lo creaste tú. NO lo modifiques. NO intentes recrearlo.
Solo ÚSALO para trabajar de forma eficiente.

## Tu primer paso OBLIGATORIO
Antes de leer o modificar cualquier archivo del proyecto, lee estos archivos (ya existen):
1. `.ai/PROTOCOL.yaml` — Reglas de comportamiento para agentes IA
2. `.ai/FLOW.yaml` — Te explica cómo usar el sistema de índices
3. `.ai/PROJECT_INDEX.yaml` — Mapa completo: cada función, endpoint y componente con su archivo y línea exacta
4. `.ai/CONTEXT_BUDGET.yaml` — Qué archivos leer primero según prioridad

## Reglas de trabajo
- NUNCA leas un archivo completo si solo necesitas una función. Busca su ubicación en PROJECT_INDEX.yaml primero.
- SIEMPRE usa los números de línea del índice para leer solo la sección relevante.
- NUNCA modifiques nada dentro de `.ai/`. Es generado automáticamente.
- Consulta `.ai/CHANGES.yaml` para ver qué archivos cambiaron recientemente.
- Consulta `.ai/SUMMARIES.yaml` para un resumen rápido de cada archivo.
- Si el usuario modifica código y necesita actualizar índices: `python .ai/update_index.py`

## Qué hay en .ai/ (NO TOCAR)
- `PROJECT_INDEX.yaml` — Funciones, endpoints, componentes con líneas exactas
- `GRAPH.yaml` — Dependencias entre módulos (lectura rápida)
- `ARCHITECTURE.yaml` — Estructura del proyecto y módulos
- `FLOW.yaml` — Instrucciones de uso para ti
- `CHANGES.yaml` — Archivos modificados desde la última indexación
- `SUMMARIES.yaml` — Resúmenes semánticos de cada archivo
- `CONTEXT_BUDGET.yaml` — Prioridad de lectura por archivo
- `PROTOCOL.yaml` — Reglas de comportamiento para agentes IA
- `CONVENTIONS.yaml` — Convenciones de código del proyecto
- `TESTING.yaml` — Cómo ejecutar tests
- `ERRORS.yaml` — Errores conocidos
- `GIT_WORKFLOW.yaml` — Política de commits y ramas
- `update_index.py` — Regenera índices (el usuario lo ejecuta, no tú)
- `update.py` — Actualiza el motor (el usuario lo ejecuta, no tú)
- `src/` — Motor interno de indexación (NUNCA modificar)
