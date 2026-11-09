# Class 04 — AI Agents: ReAct & Plan-and-Execute

## Overview

La cuarta clase introduce los fundamentos de los **agentes de inteligencia artificial**, diferenciando los workflows tradicionales de los sistemas donde un modelo de lenguaje decide dinámicamente qué acciones ejecutar.

El Agente Operador incorpora dos estrategias de ejecución: **ReAct** y **Plan-and-Execute**, junto con mecanismos para controlar el consumo de recursos, registrar decisiones y limitar la ejecución de los agentes.

### Concepts

- Diferencias entre workflows y agentes.
- Arquitectura ReAct: razonamiento, acción y observación.
- Plan-and-Execute: planificación, ejecución y replanificación.
- Presupuestos de tokens, costos, pasos y tiempo.
- Motivos de parada y detección de falta de progreso.
- Trazabilidad y observabilidad de agentes.
- Comparación de estrategias de ejecución.

## Starter Code

**Upstream commit:** [`9301364`](https://github.com/RamsesCamas/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/commit/93013643391c430c8412b4fbdcc5b004c3c70d94)

**Starter branch:** `chore/class-04-starter`

**Starter PR:** [PR #9 — Integrate Class 04 starter components](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/9)

El código base de la clase 4 se incorporó selectivamente desde el repositorio del instructor, conservando las implementaciones personales de las clases anteriores.

No se fusionó directamente `upstream/main` con `develop`, evitando incorporar soluciones publicadas posteriormente.

### Components

| Component | Responsibility |
|---|---|
| `agents/react_agent.py` | Implementación del ciclo ReAct. |
| `agents/planner.py` | Planificación, ejecución y replanificación de tareas. |
| `agents/budget.py` | Control de límites de pasos, tokens, costos y tiempo. |
| `agents/trace.py` | Registro de pasos y observaciones del agente. |
| `core/usage.py` | Seguimiento del consumo mediante `UsageMeter`. |
| `core/llm_client.py` | Integración del seguimiento de consumo en las llamadas LLM. |
| `core/logger.py` | Registro de metadatos asociados a la ejecución de agentes. |
| `prompts/react_agent/` | Plantillas para la estrategia ReAct. |
| `prompts/planner/` | Plantillas para planificación y ejecución. |
| `scripts/compare_agents.py` | Comparación de estrategias de ejecución. |
| `scripts/compare_structured.py` | Comparación de métodos de salida estructurada. |
| `tests/` | Pruebas de presupuestos, agentes y planificación. |

### Agent Strategies

**ReAct**

El agente sigue un ciclo de razonamiento, acción y observación.

En cada paso, el modelo decide si debe ejecutar una herramienta o responder al usuario. Los resultados de las herramientas se incorporan al contexto de los pasos siguientes.

**Plan-and-Execute**

El agente genera primero un plan de ejecución y posteriormente resuelve sus pasos utilizando agentes ejecutores.

La arquitectura contempla replanificación cuando un paso falla y utiliza un presupuesto global para controlar el consumo de recursos.

### Execution Budget

El starter incorpora límites explícitos para evitar ejecuciones indefinidas.

| Resource | Default limit |
|---|---:|
| Agent steps | 6 |
| Tokens | 12,000 |
| Estimated cost | $0.02 USD |
| Execution time | 45 seconds |

Los límites pueden detener la ejecución cuando el agente consume el presupuesto disponible o supera el tiempo permitido.

## Activity

La práctica de la clase 4 se enfoca en mejorar la detección de agentes que repiten acciones sin producir información nueva.

### Requirements

1. Detectar cuando el agente solicita repetidamente la misma herramienta con los mismos argumentos.
2. Evitar continuar una ejecución que no produce progreso.
3. Registrar el motivo de parada `sin_progreso`.
4. Mantener los mecanismos existentes de presupuesto y trazabilidad.
5. Validar el comportamiento mediante los escenarios de ejecución correspondientes.

La solución debe integrarse en la arquitectura existente sin modificar innecesariamente las estrategias de planificación o ejecución.

### Expected Behavior

Un agente que repite una acción sin obtener información nueva debe detenerse de forma controlada, en lugar de consumir indefinidamente pasos, tokens y presupuesto.

## Personal Implementation

**Branch:** `feat/class-04`

**Status:** Completed

**Pull Request:** [PR #10 — Add `sin_progreso` exit case to agents](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/10)

### No-Progress Detection

Se implementó la detección de ejecuciones repetitivas dentro de `AgentBudget.exhausted()` en `agents/budget.py`.

La solución compara los dos últimos pasos registrados en la traza del agente, verificando:

- Que existan al menos dos pasos.
- Que ambos utilicen la misma herramienta.
- Que los argumentos JSON sean idénticos.

Cuando se cumplen estas condiciones, el presupuesto devuelve el motivo de parada `sin_progreso`.

La implementación aprovecha el mecanismo de presupuesto existente, sin introducir nuevos ciclos de ejecución ni modificar la arquitectura de ReAct.

### Design Decisions

- Se reutilizó `AgentBudget.exhausted()` como punto central de validación.
- La detección compara los argumentos JSON tal como fueron registrados, sin normalización adicional.
- No se modificó `exhausted_totals()`, utilizado por Plan-and-Execute para controlar presupuestos agregados.
- Se conservaron los límites existentes de pasos, tokens, costos y tiempo.

## Validation & Results

**Status:** Completed

### Automated Tests

Se incorporaron tres pruebas:

| Test                                 | Expected Behavior                                                                  |
| ------------------------------------ | ---------------------------------------------------------------------------------- |
| `test_sin_progreso`                  | Dos llamadas consecutivas idénticas devuelven `sin_progreso`.                      |
| `test_same_tool_call_different_args` | La misma herramienta con argumentos diferentes no activa la detección.             |
| `test_stops_when_no_progress`        | ReAct se detiene después de dos llamadas repetidas y registra el motivo de parada. |

La prueba de integración utiliza un proveedor simulado (`FakeProvider`) para reproducir llamadas consecutivas a `buscar_ticket` con el mismo identificador.

### Results

Los escenarios automatizados verifican que:

1. `AgentBudget` detecta llamadas consecutivas repetidas.
2. Las llamadas con argumentos distintos no se consideran repetidas.
3. `ReActAgent` finaliza con el motivo `sin_progreso`.
4. La traza conserva los dos pasos ejecutados.
5. El log registra `stop_reason: sin_progreso`.

### Validation Commands

```bash
uv run pytest tests/test_budget.py tests/test_react_agent.py -q
just check
```

Estas verificaciones permiten comprobar la detección de falta de progreso y la compatibilidad con las funcionalidades existentes.

### Limitations

La detección utiliza una comparación exacta de los argumentos JSON.

Dos llamadas semánticamente equivalentes podrían no identificarse como repetidas si sus argumentos utilizan diferentes representaciones JSON.

Asimismo, la implementación detecta llamadas consecutivas, no patrones repetitivos separados por otras acciones.

## Milestone

**Tag:** `class-04`

**Starter PR:** [#9](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/9)

**Activity PR:** [#10](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/10)

La implementación de la clase 4 se integró en `develop` mediante el PR #10.
