shell:
	docker-compose run jarvis

up:
	docker-compose up -d

stop:
	docker-compose stop

build:
	docker-compose up --build -d

compile:
	pip-compile

compile-b:
	pip-compile --rebuild

install:
	pip-sync requirements.txt

venv:
	python3 -m venv py-jarvis

activate:
	source py-jarvis/bin/activate