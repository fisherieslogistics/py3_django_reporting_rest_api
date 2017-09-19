ENV=~/fllenv
ENV_BIN=$(ENV)/bin/
setup:
	python3 -m venv $(ENV)
	$(ENV_BIN)pip install -r requirements_frozen.txt

build-docker: setup
	rm -rf build
	$(ENV_BIN)python manage.py collectstatic
	docker build -t fisherylogistics/rest-api:latest .
	rm -rf build
	docker push fisherylogistics/rest-api:latest

build-docker-fishserve:
	docker build -f Dockerfile.fishserve -t fisherylogistics/fishserve-sender:latest .
	docker push fisherylogistics/fishserve-sender

upgrade-libs:
	rm -rf .fllenv_upgrade
	python3 -m venv .fllenv_upgrade
	.fllenv_upgrade/bin/pip install -r requirements.txt
	.fllenv_upgrade/bin/pip freeze >requirements_frozen.txt
	rm -rf .fllenv_upgrade

test-rest:
	$(ENV_BIN)pip install -r requirements_tests.txt
	- python manage.py shell <reporting/tests/prepare_test_database.py
	cd reporting/tests && $(ENV_BIN)resttest.py http://localhost:8000 all.yaml --import_extensions 'dategen;geojsonpoint'

migrate:
	$(ENV_BIN)python manage.py migrate
	$(ENV_BIN)python manage.py loaddata reporting/migrations/data/groups.json
	$(ENV_BIN)python manage.py loaddata reporting/migrations/data/species.json
