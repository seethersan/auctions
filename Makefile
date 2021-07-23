CONTAINER_NAME = auctions

status: ## Show containers status, use me with: make status target=api
	docker-compose ps ${target}

stop: ## Stops the docker containers, use me with: make stop target=api
	docker-compose stop ${target}

down: ## Stops and removes the docker containers, use me with: make down target=api
	docker-compose down ${target}

delete: ## Delete the docker containers, use me with: make delete target=api
	docker-compose rm -fv ${target}

d.build: ## Build the docker containers, use me with: make build target=api
	docker-compose build ${target}

up: ## Up the docker containers, use me with: make up target=api
	docker-compose up -d ${target}

logs: ## Logss the docker containers, use me with: make logs target=api
	docker-compose logs -f ${target}

restart: ## Restart the docker containers, use me with: make restart target=api
	docker-compose restart ${target}

rebuild: # Rebuild the docker containers, use me with: make rebuild
	make stop
	make delete
	make d.build
	make up

init: # Init the docker containers, use me with: make init
	sleep 5
	docker exec ${CONTAINER_NAME}_web_1 python manage.py migrate
	sleep 5
	docker exec -it ${CONTAINER_NAME}_web_1 python manage.py createsuperuser

test: # Run django tests: make init
	sleep 5
	docker exec ${CONTAINER_NAME}_web_1 python manage.py test