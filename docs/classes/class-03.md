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

**Pull Request:** [PR #8 — consultar_proveedor tool](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/8)

Se implementó una segunda herramienta para consultar información de proveedores y permitir que el Agente Operador combine sus resultados con los obtenidos mediante `buscar_ticket`.

### Provider Tool

Se incorporaron los siguientes componentes:

| Component | Responsibility |
|---|---|
| `ConsultarProveedorArgs` | Contrato Pydantic para recibir el nombre del proveedor. |
| `CONSULTAR_PROVEEDOR` | Definición de la herramienta mediante `ToolSpec`. |
| `tools/proveedores.py` | Consulta de información desde `data/proveedores.json`. |
| `main.py` | Registro de la nueva herramienta junto con `BUSCAR_TICKET`. |

La herramienta devuelve información como el nombre, estado, SLA, contacto y contratos vigentes del proveedor.

### Provider Name Normalization

Se incorporó una función `normalize_provider_name()` para realizar búsquedas sin depender de la capitalización o de las tildes utilizadas en los nombres.

La normalización utiliza herramientas de la biblioteca estándar de Python:

- `str.casefold()` para comparaciones sin distinguir mayúsculas y minúsculas.
- `unicodedata.normalize()` para descomponer caracteres Unicode.
- Eliminación de marcas diacríticas.
- Expresiones regulares para tratar puntuación y espacios.

Esto permite resolver variaciones como `PagosRed`, `pagosred` y `PAGOSRED` utilizando una misma clave normalizada.

La búsqueda utiliza un índice de proveedores almacenado en caché mediante `lru_cache`, evitando lecturas repetidas del archivo JSON durante el mismo proceso.

### Tool Integration

La herramienta `CONSULTAR_PROVEEDOR` se registró junto con `BUSCAR_TICKET` en el ciclo de ejecución existente.

Esto permite al modelo consultar primero un ticket, identificar su proveedor y posteriormente obtener información adicional sobre él.

## Validation & Results

Se añadieron pruebas automatizadas en `tests/test_proveedores.py` para verificar la normalización y consulta de proveedores.

### Validation

Las verificaciones del proyecto se ejecutan mediante:

```bash
just check
```

La funcionalidad de la herramienta puede probarse utilizando:

```bash
uv run main.py --tools "¿El T-1042 depende de algún proveedor? ¿Cuál es su SLA?"
```

### Functional Results

Se comprobó el funcionamiento del agente utilizando la pregunta propuesta durante la clase.

La ejecución permite combinar las herramientas `buscar_ticket` y `consultar_proveedor` dentro de una misma solicitud para recuperar información del ticket y del proveedor asociado.

Las evidencias de ejecución están disponibles en el [PR #8](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/8).

### Limitations

La consulta de proveedores utiliza coincidencia exacta después de normalizar el nombre.

Esta estrategia permite manejar diferencias de capitalización, tildes y puntuación, pero no garantiza coincidencias ante errores ortográficos, abreviaturas desconocidas o nombres alternativos.

No se incorporó fuzzy matching, manteniendo el alcance de la actividad y evitando seleccionar proveedores incorrectos por similitud.

## Milestone

**Tag:** `class-03` — Pending merge

**Starter PR:** [#7](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/7)

**Activity PR:** [#8](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/8)

El tag `class-03` se creará después de integrar el PR de la actividad en `develop`.
