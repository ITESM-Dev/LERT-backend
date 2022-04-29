.DEFAULT_GOAL := help

.PHONY: up
up: ## run the project
	@docker-compose up -d
	@docker-compose logs -f
.PHONY: stop
stop: ## stop Docker containers without removing them
	@docker-compose stop
.PHONY: down
down: ## stop and remove Docker containers
	@docker-compose down --remove-orphans
.PHONY: pipi
pipi: ## Install packages
	@docker-compose -f docker-compose.yml exec app pipenv run pipenv install -d
.PHONY: restart
restart:
	@docker-compose build --no-cache
