
Django Project setup

For OSX setup

* install python3 + pip3
  * brew doctor
  * brew update
  * brew install python3
  * sudo easy_install install pip3 <<<<<??? that didn’t work

* run docker-postgres

* install django / python things

  * pip3 update <<<<<??? that didn’t work
  * sudo pip3 install virtualenv

* setup the env
```
python3 -m venv .fllenv
source .fllenv/bin/activate
pip install -r requirements_frozen.txt
```

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

* setup the superuser
  * python3 manage.py createsuperuser
  * follow instructions in the shell
  * python3 manage.py runserver
  * have fun with the admin interface
