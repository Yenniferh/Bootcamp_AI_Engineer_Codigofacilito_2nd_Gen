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

# Linting sin modificar archivos
lint:
    uv run ruff check .

# Corregir automáticamente errores de linting
lint-fix:
    uv run ruff check --fix .

# Aplicar formato
format:
    uv run ruff format .

# Comprobar formato sin modificar archivos
format-check:
    uv run ruff format --check .

# Pruebas
test:
    uv run pytest -q

# Validaciones para CI (no modifican archivos)
check:
    just lint
    just format-check
    just test

# Validaciones para desarrollo local (aplican correcciones)
check-dev:
    just lint-fix
    just format
    just check

# Ejecutar hooks sobre todo el repositorio
hooks:
    uv run pre-commit run --all-files

# Sincronizar main con el repositorio del profesor
sync-upstream:
    git fetch upstream
    git switch main
    git merge --ff-only upstream/main
    git push origin main
