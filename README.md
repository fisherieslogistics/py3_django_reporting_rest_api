
Django Project setup

For OSX setup

* install python3 + pip3
  * brew doctor
  * brew update
  * brew install python3
  * sudo pip3 install virtualenv

* run docker-postgres

* setup the env
```
make setup
source .fllenv/bin/activate
```

* setup the superuser
  * python3 manage.py createsuperuser
  * follow instructions in the shell
  * python3 manage.py runserver
  * have fun with the admin interface
