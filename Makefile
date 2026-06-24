.PHONY: install lint format-check type test doctor reproduce-smoke validate quality

install:
	uv sync --all-groups

lint:
	uv run ruff check .

format-check:
	uv run ruff format --check .

type:
	uv run mypy src

test:
	uv run pytest

doctor:
	uv run fts doctor

reproduce-smoke:
	uv run fts reproduce-smoke

validate:
	uv run fts validate-manifest $(MANIFEST)

quality: lint format-check type test doctor reproduce-smoke
