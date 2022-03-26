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


.PHONY: run locale compile test
