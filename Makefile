
MKDOCS_MATERIAL_VERSION := 9.1.4
PORT ?= 8000

ifeq ($(shell command -v podman 2> /dev/null),)
    CONTAINER=docker
else
    CONTAINER=podman
endif

docker-run: pull-config-server generate-template
	$(CONTAINER) run --rm --name sdcio-docs -v "$$(pwd)":/docs -p ${PORT}:${PORT} --entrypoint ash squidfunk/mkdocs-material:${MKDOCS_MATERIAL_VERSION} -c 'mkdocs serve -a 0.0.0.0:${PORT}'

pull-config-server:
	if [ ! -d "config-server-repo" ]; then git clone https://github.com/sdcio/config-server.git config-server-repo ; fi
	cd config-server-repo ; git pull ; make artifacts

generate-template:
	export $$(cat versions.env | xargs) ; cat docs/user-guide/troubleshooting.tmpl.md | envsubst > docs/user-guide/troubleshooting.md
