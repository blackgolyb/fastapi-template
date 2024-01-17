export DOCKER_DEFAULT_PLATFORM=linux/amd64

install_dev_backend:
	bash scripts/install_dev backend

install_dev_frontend:
	bash scripts/install_dev frontend

up:
	docker compose -f backend/docker-compose-local.yaml up -d

down:
	docker compose -f backend/docker-compose-local.yaml down --remove-orphans