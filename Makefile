.PHONY: test run

all: test run

discover-linter=find . -type f -name "*.py" -not -path "./*/migrations/*"
discover-style-checker=find . -type f -name "*.py" -not -path "./*/migrations/*" -not -iname "*models.py*" -not -iname "*apps.py"
discover-type-checker=find . -type f -name "*.py" -not -path "./*/migrations/*" -not -iname "*models.py*" -not -iname "*apps.py"
discover-dead-code-checker=find . -type f -name "*.py" -not -path "./*/migrations/*"

pylint:
	@echo testing with pylint
	@${discover-linter} | xargs poetry run pylint

flake8:
	@echo "testing with flake8"
	@${discover-style-checker} | xargs poetry run flake8

mypy:
	@echo "testing with mypy"
	@${discover-type-checker} | xargs poetry run mypy

vulture:
	@echo "testing with vulture"
	@${discover-dead-code-checker} | xargs poetry run vulture

servertests:
	@rm project/db.sqlite3 | echo no old test db
	@poetry run python manage.py test --settings project.settings.testing

test: pylint flake8 mypy servertests
	@echo All tests successful

migrate:
	@echo Making Migrations ...
	@poetry run python manage.py makemigrations
	@echo Applying Migrations ...
	@poetry run python manage.py migrate

adminuser:
	@poetry run python manage.py createsuperuser

run: migrate
	@echo running server ...
	@poetry run python manage.py runserver
