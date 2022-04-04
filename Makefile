run:
	@poetry run python manage.py runserver

requirements:
	@poetry export -f requirements.txt --output requirements.txt

locale:
	@poetry run django-admin makemessages -l ru

compile:
	@poetry run django-admin compilemessages --ignore=env

test:
	@poetry run python manage.py test

migrate:
	@poetry run python manage.py makemigrations
	@poetry run python manage.py migrate

coverage:
	@poetry run python manage.py makemigrations
	@poetry run python manage.py migrate --fake
	@poetry run coverage run manage.py test
	@poetry run coverage xml
	@poetry run coverage report

lint:
	@poetry run flake8 task_manager


.PHONY: run locale compile test lint
