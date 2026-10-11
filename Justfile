set shell := ["bash", "-cu"]

default:
    @just --list

# Instalar dependencias
setup:
    uv sync --frozen
    uv run pre-commit install

# Ejecutar aplicación
run *args:
    uv run python main.py {{args}}

# Linting
lint:
    uv run ruff check .

# Formato
format:
    uv run ruff format .

# Comprobar formato sin modificar archivos
format-check:
    uv run ruff format --check .

# Pruebas
test:
    uv run pytest -q

# Ejecutar todos los controles de CI
check:
    just lint
    just format-check
    just test

# Ejecutar hooks sobre todo el repositorio
hooks:
    uv run pre-commit run --all-files
