export DOCKER_DEFAULT_PLATFORM=linux/amd64

install_dev_backend:
	bash scripts/install_dev backend
install_dev_frontend:
	bash scripts/install_dev frontend