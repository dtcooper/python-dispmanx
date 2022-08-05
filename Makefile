.PHONY: build
build:
	docker compose build --pull dispmanx

.PHONY: shell
shell:
	docker compose run --rm dispmanx bash

.PHONY: clean
clean:
	rm -rf dist

.PHONY: publish
publish: clean
	docker compose run --rm dispmanx poetry publish --build
