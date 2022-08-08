.PHONY: build-docker
build-docker:
	docker compose build --pull dispmanx

.PHONY: shell-docker
shell-docker:
	docker compose run --rm dispmanx bash

.PHONY: clean
clean:
	rm -rf dist

.PHONY: publish
publish: clean
	poetry publish --build

.PHONY: pre-commit
pre-commit:
	@echo "================== isort =================="
	@poetry run isort dispmanx/
	@echo "================== black =================="
	@poetry run black dispmanx/
	@echo "================== flake8 ================="
	@poetry run flake8 dispmanx/
	@echo "================== mypy ==================="
	@poetry run mypy --always-true HAVE_NUMPY dispmanx/
