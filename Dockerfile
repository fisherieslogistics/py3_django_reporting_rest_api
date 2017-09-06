# forked from from https://github.com/dockerfiles/django-uwsgi-nginx
FROM ubuntu:16.04

# Install required packages and remove the apt packages cache when done.
# TODO removed this - is it needed? apt-get upgrade -y && \ 	

RUN apt-get update && \
    apt-get install -y \
		python3 \
		python3-dev \
		python3-setuptools \
		python3-pip \
		nginx \
		supervisor \
		binutils libproj-dev gdal-bin \
		rsyslog \
	&& pip3 install -U pip setuptools && \
   rm -rf /var/lib/apt/lists/*

# install uwsgi now because it takes a little while
RUN pip3 install uwsgi

# COPY requirements.txt and RUN pip install BEFORE adding the rest of your code, this will cause Docker's caching mechanism to prevent re-installing (all your) dependencies when you made a change a line or two in your app.
COPY requirements_frozen.txt /home/docker/code/
RUN pip3 install -r /home/docker/code/requirements_frozen.txt


# copy our code
ADD . /home/docker/code/app/

# setup all the configfiles
RUN mkdir /home/docker/volatile &&\
	mv /home/docker/code/app/build/static /home/docker/volatile/static &&\
	rm -rf /home/docker/code/app/build &&\
	echo "daemon off;" >> /etc/nginx/nginx.conf &&\
	mv /home/docker/code/app/docker/nginx-app.conf /etc/nginx/sites-available/default &&\
	mv /home/docker/code/app/docker/supervisor-app.conf /etc/supervisor/conf.d/ &&\
	mv /home/docker/code/app/docker/dhparam.pem /etc/ssl/certs/ &&\
	mv /home/docker/code/app/docker/syslog.conf /etc/rsyslog.d/catchhub.conf &&\
	mv /home/docker/code/app/docker/uwsgi* /home/docker/code/ &&\
	mv /home/docker/code/app/py3_django_reporting_rest_api/settings_dist.py /home/docker/code/app/py3_django_reporting_rest_api/settings.py
	

EXPOSE 80
EXPOSE 443

WORKDIR /home/docker/code/app/

CMD ["supervisord", "-n"]
