
Django Project setup

For OSX setup

* install python3 + pip3
  * brew doctor
  * brew update
  * brew install python3
  * sudo pip3 install virtualenv

* setup the env
```
make setup
source ~/fllenv/bin/activate
```

* setup the superuser
  * python3 manage.py createsuperuser
  * follow instructions in the shell
  * python3 manage.py runserver
  * have fun with the admin interface

How to run things:
* postgres:
  * docker run -p 5432:5432 --mount source=fllpostgres_data,target=/var/lib/postgresql/data/pgdata -d --name postgres --restart always fisherylogistics/fllpostgres:latest
* couchdb:
  * docker run --rm -p 5984:5984 -v couchdb_data:/opt/couchdb/data -v couchdb_ini:/opt/couchdb/etc/local.d -d --network fllnet --name couchdb apache/couchdb:2.1
* couchpost (couchdb <-> postgres replication service)
  * python manage.py run_couch_listener --settings couchpost.settings
  * python manage.py run_post_poller --settings couchpost.settings
  * python manage.py run_document_importer --settings couchpost.settings
* fishserve integration
  * python manage.py run_sender --settings fishserve.settings
