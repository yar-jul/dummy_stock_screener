include .env
export

.SILENT:
.PHONY: help
help: ## display this help
	awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) }' $(MAKEFILE_LIST)

.PHONY: run
run: ## run all
	make -j 2 run-api run-generator

.PHONY: run-in-docker
run-in-docker: ## run all
	make -j 2 run-api-in-docker run-generator-in-docker

.PHONY: run-api
run-api: ## run api
	poetry run gunicorn --reload --bind $(HOST):$(PORT) \
	--worker-class uvicorn.workers.UvicornWorker \
	--workers $(WORKERS) --log-level $(LOG_LEVEL) --chdir backend/src api:app

.PHONY: run-api-in-docker
run-api-in-docker: ## run api in docker
	poetry run gunicorn --bind $(HOST):$(PORT) \
	--worker-class uvicorn.workers.UvicornWorker \
	--workers $(WORKERS) --log-level $(LOG_LEVEL) --chdir src api:app

.PHONY: run-generator
run-generator: ## run data generator
	poetry run python backend/src/generator.py

.PHONY: run-generator-in-docker
run-generator-in-docker: ## run data generator in docker
	poetry run python src/generator.py

.PHONY: compose-up
compose-up: ## create and start containers
	docker-compose -f docker-compose.yml --env-file .env up -d

.PHONY: compose-start
compose-start: ## start services
	docker-compose -f docker-compose.yml --env-file .env start

.PHONY: compose-restart
compose-restart: ## restart services
	docker-compose -f docker-compose.yml --env-file .env restart

.PHONY: compose-stop
compose-stop: ## stop services
	docker-compose -f docker-compose.yml --env-file .env stop

.PHONY: compose-down
compose-down: ## stop and remove containers, networks
	docker-compose -f docker-compose.yml --env-file .env down --remove-orphans

.PHONY: compose-logs
compose-logs: ## view output from containers
	docker-compose -f docker-compose.yml --env-file .env logs -f

.PHONY: compose-ps
compose-ps: ## list containers
	docker-compose -f docker-compose.yml --env-file .env ps
