
MKDOCS_MATERIAL_VERSION := 9.1.4
PORT := 8000

docker-run: pull-config-server
	docker run --rm --name sdcio-docs -v "$$(pwd)":/docs -p ${PORT}:${PORT} --entrypoint ash squidfunk/mkdocs-material:${MKDOCS_MATERIAL_VERSION} -c 'mkdocs serve -a 0.0.0.0:${PORT}'

pull-config-server:
	if [ ! -d "config-server-repo" ]; then git clone https://github.com/sdcio/config-server.git config-server-repo ; fi
	cd config-server-repo ; git pull ; make artifacts
