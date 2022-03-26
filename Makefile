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


.PHONY: run locale compile test
