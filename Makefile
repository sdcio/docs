
MKDOCS_MATERIAL_VERSION := 9.1.4
PORT ?= 8000

ifeq ($(shell command -v docker 2> /dev/null),)
    RUNTIME=podman
    # Rootless Podman uses pasta. `-p ${PORT}:${PORT}` publishes on IPv6 as well,
    # but pasta resets connections to [::1], so http://localhost:${PORT} fails
    # (typical in WSL). Bind IPv4 loopback only so browsers fall back to 127.0.0.1.
    PUBLISH_ARGS=-p 127.0.0.1:${PORT}:${PORT}
else
    RUNTIME=docker
    PUBLISH_ARGS=-p ${PORT}:${PORT}
endif

docker-run: pull-config-server generate-template
	$(RUNTIME) run --rm --name sdc-docs -v "$$(pwd)":/docs $(PUBLISH_ARGS) --entrypoint ash squidfunk/mkdocs-material:${MKDOCS_MATERIAL_VERSION} -c 'mkdocs serve -a 0.0.0.0:${PORT}'

generate-template:
	export $$(cat versions.env | xargs) ; envsubst < docs/user-guide/troubleshooting.tmpl.md > docs/user-guide/troubleshooting.md

pull-config-server:
	if [ ! -d "config-server-repo" ]; then git clone https://github.com/sdcio/config-server.git config-server-repo ; fi
	cd config-server-repo ; git pull ; make artifacts