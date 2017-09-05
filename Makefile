ENV=~/fllenv
ENV_BIN=$(ENV)/bin/
setup:
	python3 -m venv $(ENV)
	$(ENV_BIN)pip install -r requirements_frozen.txt

build-docker: setup
	rm -rf build
	$(ENV_BIN)python manage.py collectstatic
	docker build -t rest-api .
	rm -rf build
	docker tag rest-api fisherylogistics/rest-api:latest
	docker push fisherylogistics/rest-api:latest

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
