### Hexlet tests and linter status:

[![Actions Status](https://github.com/EvilMadSquirrel/python-project-lvl4/workflows/hexlet-check/badge.svg)](https://github.com/EvilMadSquirrel/python-project-lvl4/actions) [![Python CI](https://github.com/EvilMadSquirrel/python-project-lvl4/actions/workflows/pyci.yml/badge.svg)](https://github.com/EvilMadSquirrel/python-project-lvl4/actions/workflows/pyci.yml) [![Maintainability](https://api.codeclimate.com/v1/badges/7305a699c8bb053b4e8b/maintainability)](https://codeclimate.com/github/EvilMadSquirrel/python-project-lvl4/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/7305a699c8bb053b4e8b/test_coverage)](https://codeclimate.com/github/EvilMadSquirrel/python-project-lvl4/test_coverage)

Task Manager is a web application for task management, with the ability to use labels, statuses, change executors.

### Development Features:
The project is divided into separate applications for possible reuse. Each application has its own set of tests, constants, and translated strings independent of the root project.

## See my app:

[Task manager](https://evilmadsquirrel-task-manager.herokuapp.com/)

## Local installation:

```bash
pip install --user git+https://github.com/RottingHorse/python-project-lvl4
```

###### Basic usage:

The file ".env" should be created in root directory You should list there local variables:

```
SECRET_KEY='your secret here there'
```
```
ACCESS_TOKEN='token from Rollbar error tracker'
```
to install dependencies:

```bash
pip install -r requirements.txt
```

After creation of .env file the migration should be started by two commands:

```bash
python manage.py makemigrations
python manage.py migrate
```

To launch the program:

```bash
python manage.py runserver
```

Usually it started at address http://127.0.0.1:8000/

The following tools and technologies were used in the project:

| Tool                                                                     | Description                                                                                                           |
|--------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| [django](https://www.djangoproject.com/)                                 | "The web framework for perfectionists with deadlines."                                                                |
| [i18n](https://docs.djangoproject.com/en/4.0/topics/i18n/)               | "Internationalization and localization"                                                                               |
| [django unittest](https://docs.djangoproject.com/en/4.0/topics/testing/) | "Django uses the unittest module built into the Python standard library"                                              |
| [poetry](https://python-poetry.org/)                                     | "Python dependency management and packaging made easy"                                                                |
| [Github Actions](https://github.com/features/actions)                    | "Automate your workflow from idea to production"                                                                      |
| [wemake-python-styleguide](https://wemake-python-stylegui.de/en/latest/) | "Strictest and most opinionated Python linter ever."                                                                  |
| [heroku](https://www.heroku.com/)                                        | "Build data-driven apps with fully managed data services."                                                            |
| [rollbar](https://rollbar.com/)                                          | "Proactively discover, predict, and resolve errors in real-time with Rollbar’s continuous code improvement platform." |

### Questions and suggestions:
<minichev.s.l@gmail.com>
