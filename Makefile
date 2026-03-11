PYTHON      = python3
VENV        = .venv
VENV_BIN    = $(VENV)/bin
V_PYTHON    = $(VENV_BIN)/python
V_PIP       = $(V_PYTHON) -m pip

MAIN        = a_maze_ing.py
OUTPUT_FILE = mazegen-1.0.0-py3-none-any.whl

DEPENDENCIES = pytest flake8 mypy lib/mlx-2.2-py3-none-any.whl pillow

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
	@echo "Installing dependencies..."
	@$(V_PIP) install -qq $(DEPENDENCIES)
	@echo "Installing project..."
	@$(V_PIP) install -qq $(OUTPUT_FILE) --force-reinstall
	@echo "Installation complete"

run: install
	@echo "$(BLUE)Running maze generator...$(NC)\n --------------------"
	-@$(V_PYTHON) $(MAIN) config.txt

debug: install
	@$(V_PYTHON) -m pdb $(MAIN)

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

.PHONY: build install run debug lint lint-strict clean