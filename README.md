
Django Project setup

For OSX setup

* install python3 + pip3
  * brew doctor
  * brew update
  * brew install python3
  * sudo easy_install install pip3

* install postgres App

  * download from here
  * install it from the DMG
  * https://postgresapp.com/
  * double click on the app
  * setup the path
  * sudo mkdir -p /etc/paths.d && echo /Applications/Postgres.app/Contents/Versions/latest/bin | sudo tee /etc/paths.d/postgresapp

* setup your DB
  * double-click you usernames postgres - (takes you to a psql shell)
  * CREATE DATABASE somedb;
  * create user somename with password 'somepassword';
  * GRANT ALL PRIVILEGES ON DATABASE somedb to somename;
  * alter user somename SET timezone TO 'UTC';
  * alter user somename SET default_transaction_isolation TO 'read committed';
  * alter user somename SET client_encoding TO 'utf8';

* install django / python things

  * pip3 update
  * sudo pip3 install virtualenv

* setup the env
  * python3.6 -m venv
  * source myenv/bin/activate
  * pip3 install django
  * pip3 install django-rest-framework
  * pip3 install pygments
  * pip3 install psycopg2

* make your settings.py have this in it

    * DATABASES = {
          'default': {
              'ENGINE': 'django.db.backends.postgresql_psycopg2',
              'NAME': 'somedb',
              'USER': 'myprojectuser',
              'PASSWORD': 'password',
              'HOST': 'localhost',
              'PORT': '',
          }
      }
