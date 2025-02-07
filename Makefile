install:
	uv pip sync requirements.txt

build-requirements:
	uv pip compile pyproject.toml -o requirements.txt

dev:
	flask --app example --debug run --port 8000

start:
	gunicorn --workers=4 --bind=127.0.0.1:8000 example:app

build:
	./build.sh

