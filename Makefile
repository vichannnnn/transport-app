.ONESHELL:
SHELL = bash

docker_run := docker compose run --rm
docker_backend := $(docker_run) backend

docker_production_run := docker compose -f production.docker-compose.yml run --rm
docker_production_backend := $(docker_production_run) backend


-include ./Makefile.properties

image_url = $(image_registry)/$(image_path):$(image_tag)

hello:
	echo "Hello, world!"

runproduction:
	docker compose -f production.docker-compose.yml up -d

buildproduction:
	docker compose -f production.docker-compose.yml up -d --build

runserver:
	docker exec -it backend uvicorn app.main:app --port 9000 --host 0.0.0.0 --reload

runbackend:
	docker compose -f docker-compose.yml up -d --build

runtagger:
	docker compose -f tagger.docker-compose.yml up -d --build

migrate:
	$(docker_backend) alembic upgrade head

productionmigrate:
	$(docker_production_backend) alembic upgrade head

migrations:
	$(docker_backend) alembic revision --autogenerate -m $(name)


migrateversion:
	$(docker_backend) alembic upgrade $(version)

stamp:
	$(docker_backend) alembic stamp $(version)

seed:
	$(docker_backend) python -m run_seeding

populate: seed \
	preset \
	runtagger \

preset:
	$(docker_backend) python -m preset

pylint:
	$(docker_backend) pylint ./app --disable=C0114,C0115,C0116,R0903,R0913,C0411 --extension-pkg-whitelist=pydantic --load-plugins pylint_flask_sqlalchemy

mypy:
	$(docker_backend) mypy ./app --install-types

check: pylint \
	mypy \
	tests \

tests:
	$(docker_backend) pytest ./app/tests -x -vv

# this recipe builds the docker image
image:
	docker build -t $(image_url) ./backend

# this recipe saves the docker image as a local file
image-export:
	docker save --output ./image.tar $(image_url)

# this recipe loads the docker image from a local file
image-import:
	docker load --input ./image.tar

# this recipe pushes the docker image into its repository
image-publish:
	docker push $(image_url)

