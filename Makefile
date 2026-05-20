VENV        = .venv
VENV_BIN    = $(VENV)/bin
V_PYTHON    = $(VENV_BIN)/python

MAIN        = a_maze_ing.py
VERSION     = 2.0.0
OUTPUT_FILE = mazegen-$(VERSION)-py3-none-any.whl

LOCAL_DEPS  = lib/mlx-2.2-py3-none-any.whl

FLAKE = $(VENV_BIN)/flake8
MYPY  = $(VENV_BIN)/mypy

MYPY_FLAGS = \
	--warn-return-any           \
	--warn-unused-ignores       \
	--ignore-missing-imports    \
	--disallow-untyped-defs     \
	--check-untyped-defs


install: $(OUTPUT_FILE)
	@uv sync --link-mode=copy 2> /dev/null
	@uv pip install --python $(V_PYTHON) $(LOCAL_DEPS) --link-mode=copy 2> /dev/null
	@echo "installation complete"

$(OUTPUT_FILE):
	@echo "Building project..."
	@uv build
	@cp dist/$(OUTPUT_FILE) .
	@echo "Build complete"


run: install
	uv run $(MAIN) config.txt

debug: install
	$(V_PYTHON) -m pdb $(MAIN)

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
	@$(MYPY) --strict src

profiler: install
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