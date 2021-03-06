VENV=~/fllenv
VENV_BIN=$(VENV)/bin/
BRANCH=`git rev-parse --abbrev-ref HEAD`
SUDO=

setup:
	python3 -m venv $(VENV)
	$(VENV_BIN)pip install -r requirements_frozen.txt


build-docker: setup build-docker-ubuntu build-docker-django build-docker-couchpost build-docker-fishserve build-docker-prestashop

build-docker-django:
	rm -rf build
	$(VENV_BIN)python manage.py collectstatic
	$(SUDO) docker build -t fisherylogistics/rest-api:$(BRANCH) .
	rm -rf build
	$(SUDO) docker push fisherylogistics/rest-api:$(BRANCH)

build-docker-fishserve:
	$(SUDO) docker build -f Dockerfile.fishserve -t fisherylogistics/fishserve-sender:$(BRANCH) .
	$(SUDO) docker push fisherylogistics/fishserve-sender:$(BRANCH)

build-docker-couchpost:
	$(SUDO) docker build -f Dockerfile.couchpost -t fisherylogistics/couchpost:$(BRANCH) .
	$(SUDO) docker push fisherylogistics/couchpost:$(BRANCH)

build-docker-prestashop:
	$(SUDO) docker build -f Dockerfile.prestashop -t fisherylogistics/prestashop:$(BRANCH) --build-arg BRANCH=$(BRANCH) .
	$(SUDO) docker push fisherylogistics/prestashop:$(BRANCH)

build-docker-ubuntu:
	$(SUDO) docker build -f Dockerfile.ubuntu -t fisherylogistics/ubuntu-python3:$(BRANCH) .
	$(SUDO) docker push fisherylogistics/ubuntu-python3:$(BRANCH)


upgrade-libs:
	rm -rf .fllenv_upgrade
	python3 -m venv .fllenv_upgrade
	.fllenv_upgrade/bin/pip install -r reporting/requirements.txt -r couchpost/requirements.txt -r fishserve/requirements.txt -r prestashop/requirements.txt
	.fllenv_upgrade/bin/pip freeze >requirements_frozen.txt
	rm -rf .fllenv_upgrade


test-setup: setup
	$(VENV_BIN)pip install -r requirements_tests.txt
	# junit-enabled fork of pyresttest from here: https://github.com/netjunki/pyresttest
	$(VENV_BIN)pip install  --no-index -f file://`pwd` pyresttest

test-unit:
	- kill -9 `pgrep -f testserver`  # release potential db lock
	rm -rf test-results/nose
	mkdir -p test-results/nose

	$(VENV_BIN)python manage.py test --noinput --with-xunit

	mv nosetests.xml test-results/nose/

test-rest:
	- kill -9 `pgrep -f testserver`
	rm -rf test-results/rest
	mkdir -p test-results/rest

	# TODO server log - simple redirect to a file doesn't work for some reason
	$(VENV_BIN)python manage.py testserver \
		--noinput \
		reporting/migrations/data/species.json \
		reporting/migrations/data/groups.json \
		reporting/tests/data/organisations.json \
		reporting/tests/data/users.json \
		--addrport 8001 &

	# wait for the server to start
	until nc -zv 127.0.0.1 8001 2>/dev/null; do sleep 1; done
	
	- cd reporting/tests && $(VENV_BIN)resttest.py http://localhost:8001 all.yaml --import_extensions 'dategen;geojsonpoint;uuidgen' --junit
	- mv reporting/tests/test-default.xml test-results/rest/
	- kill `pgrep -f testserver`

test: test-setup test-unit test-rest

migrate:
	$(VENV_BIN)python manage.py migrate
	$(VENV_BIN)python manage.py loaddata reporting/migrations/data/groups.json
	$(VENV_BIN)python manage.py loaddata reporting/migrations/data/species.json
