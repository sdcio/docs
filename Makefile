
MKDOCS_MATERIAL_VERSION := 9.1.4
PORT := 8000

docker-run:
	docker run --rm --name sdcio-docs -v "$$(pwd)":/docs -p ${PORT}:${PORT} --entrypoint ash squidfunk/mkdocs-material:${MKDOCS_MATERIAL_VERSION} -c 'mkdocs serve -a 0.0.0.0:${PORT}'