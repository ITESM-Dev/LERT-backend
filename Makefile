.DEFAULT_GOAL := help

.PHONY: up
up: ## run the project
	@docker-compose up -d
	@docker attach lert-backend_lert_1
.PHONY: stop
stop: ## stop Docker containers without removing them
	@docker-compose stop
.PHONY: down
down: ## stop and remove Docker containers
	@docker-compose down --remove-orphans
.PHONY: pipi
pipi: ## Install packages
	@docker-compose -f docker-compose.yml exec lert pipenv run pipenv install -d
.PHONY: rebuild
rebuild:
	@docker-compose down --remove-orphans
	@docker-compose build --no-cache
