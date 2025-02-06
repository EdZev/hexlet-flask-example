dev:
	flask --app example --debug run --port 8000

start:
	uv run gunicorn --workers=4 --bind=127.0.0.1:8000 example:app

build:
	./build.sh