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

**Status:** Pending

La implementación personal se documentará cuando se complete la actividad.

## Validation & Results

**Status:** Pending

### Validation Commands

Ejecutar las verificaciones de calidad y pruebas:

```bash
just check
```

Ejecutar el agente ReAct:

```bash
uv run main.py --agent react "Compara el estado del T-1042 y el T-1014: ¿cuál va más avanzado?"
```

Ejecutar Plan-and-Execute:

```bash
uv run main.py --agent plan "Compara el estado del T-1042 y el T-1014: ¿cuál va más avanzado?"
```

Comparar estrategias:

```bash
uv run scripts/compare_agents.py
```

Los comandos que utilizan proveedores LLM requieren credenciales válidas y pueden generar consumo de tokens.

Los resultados de la actividad y las decisiones de implementación se documentarán después de completar el reto.

## Milestone

**Tag:** `class-04` — Pending

**Starter PR:** [#9](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/9)

**Activity PR:** Pending

El tag `class-04` se creará después de integrar la implementación personal de la clase 4 en `develop`.
