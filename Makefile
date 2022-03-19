run:
	@poetry run python manage.py runserver

requirements:
	@poetry export -f requirements.txt --output requirements.txt

.PHONY: run
