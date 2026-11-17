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

Class 04 included a guided practice and an independent challenge.

### Guided Practice: No-Progress Detection

The guided practice focused on preventing ReAct agents from repeatedly executing the same tool with identical arguments.

The activity was not completed during the live session due to time constraints.

#### Requirements

1. Detect consecutive calls to the same tool with identical arguments.
2. Return `sin_progreso` as the stopping reason.
3. Preserve the existing execution budget and trace mechanisms.
4. Verify the behavior using a `FakeProvider` and automated tests.

### Independent Challenge: Response Verifier

The independent challenge was to implement a response verifier.

#### Requirements

1. Create `agents/verifier.py` with a Pydantic contract named `Verificacion`.
2. Verify that factual claims in the response are supported by the agent's trace observations.
3. Request at most one correction when verification fails.
4. Compare five questions with and without verification, measuring LLM calls, tokens, and corrected responses.

The challenge was not independently implemented. The instructor's solution was subsequently incorporated as part of the Class 05 starter.

## Personal Implementation

**Branch:** `feat/class-04`

**Status:** Guided practice completed; independent challenge not implemented.

**Pull Request:** [PR #10 - Add `sin_progreso` exit case to agents](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/10)

### Guided Practice Implementation

Implemented no-progress detection in `AgentBudget.exhausted()` within `agents/budget.py`.

The implementation examines the last two steps in the agent's trace and checks whether:

- Both steps reference the same tool.
- Both contain identical JSON arguments.

When both conditions are met, `exhausted()` returns `sin_progreso`.

This approach reuses the existing budget mechanism rather than introducing a separate detection system.

### Design Decisions

- Kept the detection inside `AgentBudget.exhausted()`.
- Compared the recorded JSON arguments directly, without additional normalization.
- Preserved existing budget limits for steps, tokens, cost, and execution time.
- Left `exhausted_totals()` unchanged because it handles aggregated budget usage rather than individual tool calls.

### Independent Challenge

The response verifier was not developed independently.

The instructor's implementation was introduced in the Class 05 starter, including `agents/verifier.py` and the corresponding verifier and reviser prompts.

## Validation & Results

**Status:** Guided practice implemented and covered by automated tests.

### Automated Tests

Three tests were added:

| Test | Expected Behavior |
|---|---|
| `test_sin_progreso` | Two identical consecutive tool calls produce `sin_progreso`. |
| `test_same_tool_call_different_args` | Different arguments do not trigger no-progress detection. |
| `test_stops_when_no_progress` | ReAct stops after two repeated calls and records `sin_progreso`. |

The integration test uses a `FakeProvider` to reproduce repeated `buscar_ticket` calls.

### Validation Commands

```bash
uv run pytest tests/test_budget.py tests/test_react_agent.py -q
just check
```

### Results

The added tests cover:

- Detection of consecutive identical tool calls.
- Avoidance of false positives when arguments differ.
- Controlled termination of the ReAct agent.
- Preservation of the execution trace.
- Recording `stop_reason: sin_progreso` in the LLM log.

### Limitations

The implementation compares JSON arguments as strings.

Semantically equivalent JSON objects with different formatting or property order may not be recognized as identical.

The detection also considers only consecutive tool calls, not repeated patterns separated by other actions.

## Milestone

**Tag:** `class-04`

**Starter PR:** [#9](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/9)

**Guided Practice PR:** [#10](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/10)

**Independent Challenge:** Not independently implemented.

The Class 04 milestone represents the completion of the guided practice and its integration into `develop`. The verifier solution was incorporated later from the instructor's code as part of the Class 05 starter.
