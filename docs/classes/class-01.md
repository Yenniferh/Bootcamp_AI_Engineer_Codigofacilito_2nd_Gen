# Class 01 — LLM Fundamentals

## Overview

La primera clase introduce los fundamentos para integrar Large Language Models (LLMs) en el proyecto **Agente Operador**.

El objetivo es construir una abstracción que permita interactuar con distintos proveedores de modelos mediante una interfaz común, incorporando mecanismos básicos de resiliencia, registro de llamadas y seguimiento de costos.

### Concepts

- Integración de proveedores LLM mediante el patrón Adapter.
- Cliente LLM con reintentos y fallback.
- Manejo de errores transitorios y permanentes.
- Logging estructurado de llamadas.
- Métricas de latencia, consumo de tokens y costos.

## Starter Code

**Upstream commit:** [`74cd808`](https://github.com/RamsesCamas/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/commit/74cd808307829f31bff8867b710c7f36f9c41838)

**Source:** [Original repository](https://github.com/RamsesCamas/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen)

El proyecto personal comenzó desde este commit, conservando la estructura inicial proporcionada por el instructor y evitando incorporar las soluciones publicadas posteriormente.

### Components

| Component | Responsibility |
|---|---|
| `core/config.py` | Configuración de proveedores y variables de entorno. |
| `core/providers.py` | Abstracción e implementaciones de proveedores LLM. |
| `core/llm_client.py` | Generación de respuestas, reintentos y fallback. |
| `core/logger.py` | Registro estructurado de llamadas. |
| `core/pricing.py` | Estimación de costos. |
| `scripts/report.py` | Base del reporte de métricas. |
| `tests/` | Pruebas automatizadas del núcleo. |

No se utilizó un Starter PR independiente para esta clase, ya que el proyecto personal se inicializó directamente desde el commit de referencia.

## Activity

La actividad consistió en completar las siguientes funcionalidades:

1. Implementar `GroqProvider` utilizando el endpoint compatible con OpenAI.
2. Verificar el mecanismo de fallback entre proveedores.
3. Completar `scripts/report.py` para procesar los registros de llamadas.
4. Calcular métricas de costo, latencia, fallback y llamadas por proveedor.
5. Manejar los casos de archivos de logs inexistentes o vacíos.

**Bonus opcional:** incorporar un parámetro `--temperature` a la CLI.

## Personal Implementation

**Branch:** `feat/class-01`

**Pull Request:** [PR #2 — Implement Groq provider and report metrics](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/2)

### Groq Provider

Se completó el adaptador de Groq utilizando la interfaz compatible con OpenAI.

La implementación reutiliza la abstracción existente para los proveedores LLM, evitando duplicar la lógica de comunicación HTTP.

### Report Metrics

Se implementó el procesamiento de registros JSONL mediante `scripts/report.py`.

La solución incluye:

- Lectura y validación básica del archivo de logs.
- Manejo de archivos inexistentes o sin eventos.
- Cálculo del costo total de las llamadas.
- Cálculo de percentiles de latencia p50 y p95.
- Cálculo del porcentaje de fallback.
- Conteo de llamadas por proveedor y por modelo.
- Presentación de resultados mediante una salida formateada.

Se separaron las responsabilidades de lectura, cálculo de métricas y presentación del reporte para facilitar las pruebas.

## Validation & Results

Se añadieron pruebas automatizadas en `tests/test_report.py` para validar el procesamiento de logs y el cálculo de métricas.

Las pruebas incluyen escenarios con:

- Archivos inexistentes y vacíos.
- Registros JSONL válidos.
- Llamadas exitosas.
- Llamadas fallidas.
- Cálculo de percentiles.
- Comportamiento del reporte ante diferentes conjuntos de eventos.

Para ejecutar las verificaciones:

```bash
just check
```

### Known Improvement

Se identificó una diferencia respecto al criterio de cálculo utilizado en la implementación de referencia del instructor.

El porcentaje de fallback debe revisarse para considerar únicamente las llamadas exitosas. Los percentiles de latencia ya se calculan a partir de eventos exitosos en la implementación del PR.

Esta mejora se realizará posteriormente en un PR independiente para evitar mezclar correcciones de clases anteriores con nuevas actividades.

## Milestone

**Tag:** [`class-01`](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/releases/tag/class-01)

**Activity PR:** [#2](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/pull/2)

**Merge commit:** [`6a03196`](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen/commit/6a031967b4b114b2cc9ee505a28646d7f4256c06)

El hito representa la implementación personal de los fundamentos del cliente LLM y las métricas iniciales del Agente Operador.
