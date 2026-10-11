VENV			= .venv
MAIN			= a_maze_ing.py
VERSION			= 2.0.0
OUTPUT_FILE		= mazegen-$(VERSION)-py3-none-any.whl

LOCAL_DEPS		= lib/mlx-2.2-py3-none-any.whl

MYPY_FLAGS		= \
	--warn-return-any           \
	--warn-unused-ignores       \
	--ignore-missing-imports    \
	--disallow-untyped-defs     \
	--check-untyped-defs

EXCLUDE_VENV	= --exclude $(VENV)

install:
	uv sync

run:
	uv run python $(MAIN) config.txt

debug:
	uv run python -m pdb $(MAIN)

build:
	uv build
	cp dist/$(OUTPUT_FILE) .

test:
	uv run pytest

lint:
	uv run flake8 . $(EXCLUDE_VENV)
	uv run mypy . $(EXCLUDE_VENV) $(MYPY_FLAGS)

lint-strict:
	uv run flake8 . $(EXCLUDE_VENV)
	uv run mypy . $(EXCLUDE_VENV) --strict

profiler:
	-uv run python -m cProfile -o profile.stats $(MAIN) config.txt "profiler"
	snakeviz profile.stats

clean:
	echo "Cleaning project..."
	uv clean
	rm -rf $(VENV) dist $(OUTPUT_FILE) profile.stats .pytest_cache output_maze.txt assets/rescaled
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	echo "Clean complete"

.PHONY: install run debug test lint lint-strict profiler clean
