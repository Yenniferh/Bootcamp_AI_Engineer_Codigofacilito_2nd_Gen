# Class 03 — Structured Outputs & Tools

## Overview

La tercera clase introduce la generación de salidas estructuradas mediante contratos Pydantic y la ejecución de herramientas solicitadas por modelos de lenguaje.

El Agente Operador incorpora mecanismos para validar respuestas, reparar salidas inválidas y consultar información operativa mediante herramientas.

### Concepts

- Structured Outputs y JSON Schema.
- Validación de respuestas mediante Pydantic.
- Reparación de respuestas que incumplen contratos.
- Function Calling y Tool Calling.
- Definición de herramientas mediante `ToolSpec`.
- Ciclos de ejecución de herramientas con límites de iteraciones.

## Starter Code

**Upstream commit:** [`f3b2a4c`](https://github.com/RamsesCamas/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/commit/f3b2a4cea74b7a9730cbeaa857cb111fa983d8c0)

**Starter branch:** `chore/class-03-starter`

**Starter PR:** [PR #7 — Integrate Class 03 starter components](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/7)

El código base de la clase 3 se incorporó selectivamente desde el repositorio del instructor, conservando las implementaciones personales de las clases anteriores.

### Components

| Component | Responsibility |
|---|---|
| `contracts/ticket.py` | Contrato Pydantic para clasificación de tickets. |
| `contracts/structured_output.py` | Generación, validación y reparación de salidas estructuradas. |
| `contracts/tool_schemas.py` | Definiciones y contratos de herramientas. |
| `contracts/tool_loop.py` | Ejecución controlada de llamadas a herramientas. |
| `tools/` | Implementación de herramientas operativas. |
| `prompts/ticket_triage/` | Prompt para clasificación estructurada. |
| `prompts/operator_tools/` | Prompt para interacción con herramientas. |
| `data/tickets_db.json` | Base de datos de tickets de ejemplo. |
| `data/proveedores.json` | Información de proveedores ficticios. |
| `tests/` | Pruebas de contratos, proveedores y herramientas. |

## Activity

La actividad consiste en incorporar una segunda herramienta al Agente Operador.

### Requirements

1. Crear `ConsultarProveedorArgs` y el `ToolSpec` `CONSULTAR_PROVEEDOR`.
2. Implementar `consultar_proveedor(nombre)` utilizando `data/proveedores.json`.
3. Registrar la herramienta en `main.py` junto con `BUSCAR_TICKET`.
4. Conseguir que el agente combine ambas herramientas para responder preguntas relacionadas con tickets y proveedores.

### Expected Behavior

El agente debe poder responder consultas como:

```bash
uv run main.py --tools "¿El T-1042 depende de algún proveedor? ¿Cuál es su SLA?"
```

La ejecución debe registrar ambas herramientas dentro de una misma solicitud.

## Personal Implementation

**Branch:** `feat/class-03`

**Status:** Pending

La implementación personal se documentará al completar la actividad.

## Validation & Results

**Status:** Pending

Para validar el código base:

```bash
just check
```

Para probar las capacidades iniciales:

```bash
uv run main.py --structured --ticket T-1042
uv run main.py --tools "¿Cómo va el T-1042?"
```

Las llamadas reales a modelos requieren proveedores configurados y credenciales válidas.

Los resultados de la actividad se añadirán cuando esté completada.

## Milestone

**Tag:** `class-03` — Pending

**Starter PR:** [#7](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/7)

**Activity PR:** Pending

El tag se creará después de integrar la implementación personal de la clase 3 en `develop`.
