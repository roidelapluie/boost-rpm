el7-rpm:
	docker run -e XUID="$(shell id -u)" --rm -v $(shell pwd):/work -w /work -ti fedora:23 /work/dockerscript.sh
