set dotenv-load := true

default: install lint build test

# Variables
compose := "docker compose"
service := "application"
alembic := "uv run alembic"
pytest := "uv run pytest"
watch := "uv run pytest-watch --wait tests app --runner"

# Bring down docker-compose services
down:
    {{compose}} down --remove-orphans

# Open a shell in the application container
sh *args:
    {{compose}} run --service-ports {{service}} sh -c "{{args}}"

# Run tests with database reset
test *args:
    {{compose}} run {{service}} sh -c "sleep 1 && {{alembic}} downgrade base && {{alembic}} upgrade head && {{pytest}} {{args}}"

# Run tests in test-driven development mode
tdd:
    {{compose}} run {{service}} sh -c "sleep 1 && {{alembic}} downgrade base && {{alembic}} upgrade head && {{watch}} '{{pytest}} --stepwise --no-cov-on-fail --showlocals'"

# Run the application
run:
    {{compose}} run --service-ports {{service}} sh -c "sleep 1 && {{alembic}} upgrade head && uv run python -m app"

# Create a new migration
migration *args:
    {{compose}} run {{service}} sh -c "sleep 1 && {{alembic}} upgrade head && {{alembic}} revision --autogenerate {{args}}"

# Build the application using Docker Buildx Bake
build:
    docker buildx bake

# Install dependencies
install:
    uv lock --upgrade
    uv sync --all-extras --no-install-project --frozen

# Lint the codebase
lint:
    uv run ruff format .
    uv run ruff check . --fix
    uv run mypy .
