# Bootcamp AI Engineer — Class Documentation

Documentación del progreso académico y técnico de mi implementación personal del proyecto **Agente Operador**, desarrollado durante el Bootcamp AI Engineer con Python — 2ª Edición de Código Facilito.

Este directorio registra la evolución del proyecto, diferenciando el código base proporcionado por el instructor de las soluciones desarrolladas de manera independiente.

## Class Progress

| Class | Topic | Status | Documentation |
|---|---|---|---|
| 01 | LLM Fundamentals | Completed | [Class 01](classes/class-01.md) |
| 02 | Prompt & Context Engineering | Completed | [Class 02](classes/class-02.md) |
| 03 | Structured Outputs & Tools | Pending | — |

Las clases siguientes se incorporarán a este índice conforme avance el bootcamp.

## Documentation Structure

Cada clase cuenta con un archivo Markdown independiente ubicado en `docs/classes/`.

Los documentos siguen una estructura común:

| Section | Description |
|---|---|
| Overview | Conceptos y objetivos de la clase. |
| Starter Code | Commit de referencia del instructor y componentes incorporados. |
| Activity | Requisitos de la actividad asignada. |
| Personal Implementation | Solución desarrollada, decisiones técnicas y PR. |
| Validation & Results | Pruebas, métricas y resultados obtenidos. |
| Milestone | Tag que identifica el estado final de la clase. |

## Development Workflow

El proyecto utiliza un workflow acumulativo con separación entre el código del instructor y la implementación personal.

- **`main`**: referencia sincronizada con el repositorio original.
- **`develop`**: implementación personal acumulativa.
- **`chore/class-XX-starter`**: integración selectiva del código base de una clase, cuando sea necesario.
- **`feat/class-XX`**: desarrollo de la actividad correspondiente.
- **`class-XX`**: tag que identifica el estado del proyecto al completar una clase.

Cada actividad se integra mediante Pull Request hacia `develop`, después de superar las verificaciones de integración continua.

## Traceability

La documentación permite seguir el desarrollo de cada clase a través de cuatro referencias:

1. **Upstream commit:** estado del código del instructor utilizado como punto de partida.
2. **Starter PR:** incorporación de componentes base a la implementación personal, cuando corresponde.
3. **Activity PR:** cambios realizados para completar la actividad.
4. **Class tag:** estado integrado del proyecto al finalizar la clase.

Esta separación facilita revisar decisiones de implementación, comparar soluciones y recuperar hitos anteriores sin mezclar el historial académico con el desarrollo personal.

## References

- [Project README](../README.md)
- [Original repository](https://github.com/RamsesCamas/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen)
- [Personal implementation](https://github.com/Yenniferh/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen)
