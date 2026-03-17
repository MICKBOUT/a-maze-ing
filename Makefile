UV          = $(HOME)/.local/bin/uv
VENV        = .venv
VENV_BIN    = $(VENV)/bin
V_PYTHON    = $(VENV_BIN)/python

MAIN        = a-maze-ing.py
VERSION     = 1.0.0
OUTPUT_FILE = mazegen-$(VERSION)-py3-none-any.whl
STAMP       = $(VENV)/.install.stamp
VENV_STAMP  = $(VENV)/.venv.stamp

LOCAL_DEPS  = lib/mlx-2.2-py3-none-any.whl

FLAKE = $(VENV_BIN)/flake8
MYPY  = $(VENV_BIN)/mypy

RED=\033[0;31m
GREEN=\033[0;32m
BLUE=\033[0;34m
NC=\033[0m

MYPY_FLAGS = \
	--warn-return-any           \
	--warn-unused-ignores       \
	--ignore-missing-imports    \
	--disallow-untyped-defs     \
	--check-untyped-defs


build: $(OUTPUT_FILE)

$(UV):
	@echo "$(BLUE)uv not found, installing...$(NC)"
	@curl -Lsf https://astral.sh/uv/install.sh | sh
	@echo "$(GREEN)uv installed$(NC)"

$(VENV_STAMP): $(UV)
	@echo "Creating virtual environment..."
	@$(UV) venv $(VENV)
	@touch $(VENV_STAMP)
	@echo "Virtual environment ready"

$(OUTPUT_FILE): $(VENV_STAMP)
	@echo "Building project..."
	@$(UV) build
	@cp dist/$(OUTPUT_FILE) .
	@echo "Build complete"

$(STAMP): $(VENV_STAMP) $(OUTPUT_FILE) $(LOCAL_DEPS)
	@echo "Installing local dependencies..."
	@$(UV) pip install --python $(V_PYTHON) $(LOCAL_DEPS)
	@echo "Installing project with dependencies..."
	@$(UV) pip install --python $(V_PYTHON) -e ".[dev]"
	@touch $(STAMP)
	@echo "Installation complete"

install: $(STAMP)

run: $(STAMP)
	@echo "$(BLUE)Running maze generator...$(NC)"
	@echo "--------------------"
	-@$(V_PYTHON) $(MAIN) config.txt

debug: $(STAMP)
	@$(V_PYTHON) -m pdb $(MAIN)

test: $(STAMP)
	@echo "Running tests..."
	@$(VENV_BIN)/pytest

lint: $(STAMP)
	@echo "Running flake8..."
	@$(FLAKE) . --exclude $(VENV)
	@echo "Running mypy..."
	@$(MYPY) $(MYPY_FLAGS) src

lint-strict: $(STAMP)
	@$(FLAKE) . --exclude $(VENV)
	@$(MYPY) --strict src

clean:
	@echo "Cleaning project..."
	@rm -rf $(VENV) dist $(OUTPUT_FILE)
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@rm -rf .pytest_cache output_maze.txt
	@rm -rf assets/rescaled
	@echo "Clean complete"

.PHONY: all build install run debug test lint lint-strict clean