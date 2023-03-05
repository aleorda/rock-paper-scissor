start: build up

build:
	docker compose build

up:
	docker compose up -d --remove-orphans

halt:
	docker compose down

recreate: halt
	docker compose up -d --force-recreate --build --remove-orphans

safety:
	docker compose exec rps safety check

make-migration:
	docker compose exec rps app/mangae.py makemigrations

migrate:
	docker compose exec rps app/mangae.py migrate

test:
	docker compose exec rps coverage run -m pytest
	docker compose exec rps coverage report

coverage: test
	docker compose exec rps coverage html open htmlcov/index.html
