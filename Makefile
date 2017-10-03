VENV=~/fllenv
VENV_BIN=$(VENV)/bin/
setup:
	python3 -m venv $(VENV)
	$(VENV_BIN)pip install -r requirements_frozen.txt

build-docker: setup
	rm -rf build
	$(VENV_BIN)python manage.py collectstatic
	docker build -t fisherylogistics/rest-api:latest .
	rm -rf build
	docker push fisherylogistics/rest-api:latest

build-docker-fishserve:
	docker build -f Dockerfile.fishserve -t fisherylogistics/fishserve-sender:latest .
	docker push fisherylogistics/fishserve-sender

build-docker-couchpost:
	docker build -f Dockerfile.couchpost -t fisherylogistics/couchpost:latest .
	docker push fisherylogistics/couchpost:latest

upgrade-libs:
	rm -rf .fllenv_upgrade
	python3 -m venv .fllenv_upgrade
	.fllenv_upgrade/bin/pip install -r requirements.txt
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
