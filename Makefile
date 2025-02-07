install:
	curl -LsSf https://astral.sh/uv/install.sh | sh
	uv venv
	source $HOME/.local/bin/env
	uv sync

build-requirements:
	uv pip compile pyproject.toml -o requirements.txt

dev:
	flask --app example --debug run --port 8000

prod:
	uv run gunicorn --workers=4 --bind 0.0.0.0:$(PORT) example:app

build:
	./build.sh

