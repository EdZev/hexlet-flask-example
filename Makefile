install:
	curl -LsSf https://astral.sh/uv/install.sh | sh
	uv venv
	source .venv/bin/activate
	uv sync

build-requirements:
	uv pip compile pyproject.toml -o requirements.txt

dev:
	flask --app example --debug run --port 8000

prod:
	uv run gunicorn --workers=4 --bind 0.0.0.0:$(PORT) example:app

render-start:
	gunicorn --workers=4 --bind 0.0.0.0:$(PORT) example:app

render-build:
	pip install -r requirements.txt
	export DATABASE_URL="postgresql://hexlet_test_nmp3_user:NvNGqTtLC1djycfsiB6iWRZws5fvf6Lb@dpg-cuiq3uan91rc73bll6ig-a/hexlet_test_nmp3"
	./build.sh

