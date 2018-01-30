# git branch passed from Makefile
ARG BRANCH=master
FROM fisherylogistics/ubuntu-python3:$BRANCH

# install uwsgi now because it takes a little while
RUN pip3 install uwsgi

# copy our code
ADD . /home/docker/code/app/

# setup all the configfiles
RUN mkdir /home/docker/volatile &&\
	mv /home/docker/code/app/build/static /home/docker/volatile/static &&\
	rm -rf /home/docker/code/app/build &&\
	echo "daemon off;" >> /etc/nginx/nginx.conf &&\
	mv /home/docker/code/app/docker/nginx-app.conf /etc/nginx/sites-available/default &&\
	mv /home/docker/code/app/docker/supervisor-app.conf /etc/supervisor/conf.d/ &&\
	mv /home/docker/code/app/docker/syslog.conf /etc/rsyslog.d/catchhub.conf &&\
	mv /home/docker/code/app/docker/uwsgi* /home/docker/code/ &&\
	mv /home/docker/code/app/py3_django_reporting_rest_api/settings_dist.py /home/docker/code/app/py3_django_reporting_rest_api/settings.py &&\
	mv /home/docker/code/app/fishserve/settings_dist.py /home/docker/code/app/fishserve/settings.py
	

EXPOSE 80

WORKDIR /home/docker/code/app/

CMD ["supervisord", "-n"]
