shell:
	docker-compose run jarvis

up:
	docker-compose up -d

stop:
	docker-compose stop

build:
	docker-compose up --build -d