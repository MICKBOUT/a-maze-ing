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


install: $(OUTPUT_FILE)
	uv sync
	@$(UV) pip install --python $(V_PYTHON) $(LOCAL_DEPS)


$(OUTPUT_FILE):
	@echo "Building project..."
	@$(UV) build
	@cp dist/$(OUTPUT_FILE) .
	@echo "Build complete"


run: build
	uv run $(MAIN) config.txt

debug: build
	@$(V_PYTHON) -m pdb $(MAIN)

test: build
	@echo "Running tests..."
	@$(VENV_BIN)/pytest

lint: build
	@echo "Running flake8..."
	@$(FLAKE) . --exclude $(VENV)
	@echo "Running mypy..."
	@$(MYPY) $(MYPY_FLAGS) src

lint-strict: build
	@$(FLAKE) . --exclude $(VENV)
	@$(MYPY) --strict src

profiler: build
	-@$(V_PYTHON) -m cProfile -o profile.stats $(MAIN) config.txt "profiler"
	snakeviz profile.stats

clean:
	@echo "Cleaning project..."
	@uv clean
	@rm -rf $(VENV) dist $(OUTPUT_FILE)
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@rm -rf .pytest_cache output_maze.txt
	@rm -rf assets/rescaled
	@echo "Clean complete"

.PHONY: install run debug test lint lint-strict profiler clean