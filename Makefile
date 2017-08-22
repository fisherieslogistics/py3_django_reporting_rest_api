ENV=.fllenv
ENV_BIN=$(ENV)/bin/
setup:
	python3 -m venv $(ENV)
	$(ENV_BIN)pip install -r requirements_frozen.txt

build-docker: setup
	rm -rf build
	$(ENV_BIN)python manage.py collectstatic
	docker build -t django_rest_api .
	rm -rf build

upgrade-libs:
	rm -rf .fllenv_upgrade
	python3 -m venv .fllenv_upgrade
	.fllenv_upgrade/bin/pip install -r requirements.txt
	.fllenv_upgrade/bin/pip freeze >requirements_frozen.txt
	rm -rf .fllenv_upgrade