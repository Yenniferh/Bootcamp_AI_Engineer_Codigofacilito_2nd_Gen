# Class 02 — Prompt & Context Engineering

## Overview

La segunda clase introduce técnicas de **Prompt Engineering** y **Context Engineering** para mejorar la calidad, consistencia y confiabilidad de las respuestas generadas por modelos de lenguaje.

El Agente Operador incorpora mecanismos para gestionar prompts versionados, controlar el contexto enviado a los modelos y evaluar distintas estrategias de clasificación de tickets.

### Concepts

- Prompt templates con Jinja2.
- Versionamiento de prompts mediante YAML.
- Zero-shot y few-shot prompting.
- Gestión de presupuestos de tokens.
- Evaluación de precisión y costos.
- Prompt injection y delimitación de instrucciones.

## Starter Code

**Upstream commit:** [`e368f638`](https://github.com/RamsesCamas/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/commit/e368f638169ea65c23eb2528a43e48f96b8453e5)

**Starter branch:** `chore/class-02-starter`

**Starter PR:** [PR #4 — Integrate Class 02 starter components](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/4)

El código base de la clase 2 se incorporó de manera selectiva desde el repositorio del instructor, conservando la implementación personal de la clase 1.

No se fusionó directamente `upstream/main` con `develop`.

### Components

| Component | Responsibility |
|---|---|
| `prompting/promptkit.py` | Carga y renderizado de prompts versionados. |
| `prompts/ticket_classifier/` | Versiones iniciales del clasificador. |
| `context/manager.py` | Gestión de contexto con presupuesto de tokens. |
| `scripts/compare_prompts.py` | Evaluación comparativa de prompts. |
| `scripts/context_demo.py` | Demostración de gestión del contexto. |
| `data/tickets_etiquetados.jsonl` | Dataset de evaluación con 20 tickets. |
| `data/tickets_ataque.jsonl` | Casos de prueba de prompt injection. |
| `tests/` | Pruebas de los componentes incorporados. |

### Dependencies

Se añadieron dos dependencias:

- **Jinja2:** renderizado de plantillas de prompts.
- **PyYAML:** lectura y procesamiento de archivos YAML.

Las dependencias se incorporaron mediante `uv`, manteniendo actualizado `uv.lock`.

## Activity

La actividad de la clase 2 consistió en:

1. Migrar el system prompt del operador desde `main.py` hacia una plantilla YAML versionada.
2. Cargar el prompt mediante `PromptKit`.
3. Comparar las versiones v1 y v2 del clasificador utilizando el dataset etiquetado.
4. Crear una versión v3 utilizando few-shot prompting.
5. Evaluar precisión, tokens promedio, costo estimado por 1.000 tickets y resistencia a prompt injection.

El objetivo era mejorar los resultados del clasificador sin modificar innecesariamente la infraestructura proporcionada durante la clase.

## Personal Implementation

**Branch:** `feat/class-02`

**Pull Request:** [PR #5 — Load system prompt with PromptKit and add v3 few-shot](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/5)

### Operator Assistant Prompt

Se migró el system prompt del operador desde una constante en `main.py` hacia:

`prompts/operator_assistant/v1.yaml`

La aplicación utiliza `PromptKit` para cargar y renderizar la plantilla.

Esto permite separar las instrucciones del modelo de la lógica de la aplicación.

### Ticket Classifier v3

Se creó:

`prompts/ticket_classifier/v3.yaml`

La nueva versión incorpora ejemplos few-shot para mejorar la clasificación de tickets, especialmente en categorías ambiguas y escenarios de prompt injection.

La plantilla utiliza los ejemplos disponibles mediante la variable `examples`, conservando el mecanismo de renderizado de `PromptKit`.

Se mantuvo `examples` fuera de las claves globalmente obligatorias del esquema, ya que no todas las plantillas requieren ejemplos.

### Prompt Versioning

Se configuró v3 como versión activa del clasificador.

Las versiones v1 y v2 permanecen disponibles para evaluaciones y comparaciones posteriores.

También se actualizaron las pruebas existentes para comprobar la carga de las tres versiones y la selección del prompt activo.

## Validation & Results

Se evaluaron las tres versiones del clasificador utilizando 20 tickets etiquetados y cinco casos de prompt injection.

### Evaluation Results

| Metric | v1 | v2 | v3 |
|---|---:|---:|---:|
| Correct classifications | 16/20 | 18/20 | 20/20 |
| Accuracy | 80% | 90% | 100% |
| Average tokens | 68 | 183 | 500 |
| Estimated cost / 1K tickets | $0.0259 | $0.0601 | $0.1547 |
| Attacks resisted | 2/5 | 4/5 | 5/5 |

### Observations

**Accuracy**

La versión v3 clasificó correctamente los 20 tickets del conjunto de evaluación.

En comparación con v2, corrigió las clasificaciones de los tickets `T-2018` y `T-2020`, correspondientes a la categoría `otro`.

**Prompt Injection**

La versión v3 resistió los cinco casos de ataque evaluados.

En particular, corrigió el comportamiento observado en v2 para el ticket `T-1103`.

**Token Consumption & Cost**

La mejora en precisión y resistencia a ataques estuvo acompañada de un mayor consumo de tokens.

El costo estimado de v3 por 1.000 tickets fue aproximadamente 2,6 veces el de v2.

Esto representa un compromiso entre calidad y costo que debe considerarse al seleccionar prompts para entornos de producción.

### Limitations

Los resultados corresponden a un conjunto de evaluación pequeño.

Con 20 tickets, cada clasificación correcta representa cinco puntos porcentuales de precisión.

Por tanto, obtener un 100% de precisión en esta evaluación no garantiza el mismo rendimiento con otros datasets, modelos o escenarios de producción.

Los detalles de las clasificaciones incorrectas y la comparación entre versiones están documentados en el [PR #5](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/5).

### Validation Commands

Ejecutar las pruebas y verificaciones de calidad:

```bash
just check
```

Comparar las tres versiones:

```bash
uv run scripts/compare_prompts.py ticket_classifier --versions 1 2 3
```

Ejecutar la demostración del ContextManager:

```bash
uv run scripts/context_demo.py
```

Las evaluaciones que utilizan proveedores LLM requieren las credenciales correspondientes en `.env`.

## Milestone

**Tag:** [`class-02`](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/releases/tag/class-02)

**Starter PR:** [#4](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/4)

**Activity PR:** [#5](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/5)

**Merge commit:** [`5571e00`](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/commit/5571e00e3410f4043bf182ec6b66778ebc7f3d77)

El hito representa la incorporación de prompts versionados, gestión de contexto y una implementación personal de few-shot prompting evaluada mediante métricas de precisión, consumo y resistencia a ataques.
