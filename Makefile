PYTHON      = python3
VENV        = .venv
VENV_BIN    = $(VENV)/bin
V_PYTHON    = $(VENV_BIN)/python
V_PIP       = $(V_PYTHON) -m pip

MAIN        = a_maze_ing.py
VERSION     = 1.0.0
OUTPUT_FILE = mazegen-$(VERSION)-py3-none-any.whl

LOCAL_DEPS  = lib/mlx-2.2-py3-none-any.whl

FLAKE = $(VENV_BIN)/flake8
MYPY  = $(VENV_BIN)/mypy

RED=\033[0;31m
GREEN=\033[0;32m
BLUE=\033[0;34m
NC=\033[0m

MYPY_FLAGS = \
	--warn-return-any			\
	--warn-unused-ignores		\
	--ignore-missing-imports	\
	--disallow-untyped-defs		\
	--check-untyped-defs

$(VENV):
	@echo "Creating virtual environment..."
	@$(PYTHON) -m venv $(VENV)
	@$(V_PIP) install -q --upgrade pip
	@echo "Virtual environment ready"

build: $(OUTPUT_FILE)

$(OUTPUT_FILE):
	@echo "Building project..."
	@rm -rf build_venv
	@$(PYTHON) -m venv build_venv
	@. build_venv/bin/activate && \
		python -m pip install -q build && \
		python -m build
	@rm -rf build_venv
	@cp dist/$(OUTPUT_FILE) .
	@echo "Build complete"

install: build $(VENV)
	@echo "Installing local dependencies..."
	@$(V_PIP) install -qq $(LOCAL_DEPS)
	@echo "Installing project with dependencies..."
	@$(V_PIP) install -qq -e ".[dev]"
	@echo "Installation complete"

run: install
	@echo "$(BLUE)Running maze generator...$(NC)\n --------------------"
	-@$(V_PYTHON) $(MAIN) config.txt

debug: install
	@$(V_PYTHON) -m pdb $(MAIN)

test: install
	@echo "Running tests..."
	@$(VENV_BIN)/pytest

lint: install
	@echo "Running flake8..."
	@$(FLAKE) . --exclude $(VENV)
	@echo "Running mypy..."
	@$(MYPY) $(MYPY_FLAGS) src

lint-strict: install
	@$(FLAKE) . --exclude $(VENV)
	@$(MYPY) $(MYPY_FLAGS) --strict src

clean:
	@echo "Cleaning project..."
	@rm -rf $(VENV) build_venv dist $(OUTPUT_FILE)
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@rm -rf .pytest_cache output_maze.txt
	@echo "Clean complete"

.PHONY: build install run debug test lint lint-strict clean