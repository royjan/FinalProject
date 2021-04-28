
# load any public updates from python packages
FROM python:3

# upgrade any existing packages that can been updated
RUN apt-get -y upgrade

# make a directory for our application as our workdir
RUN mkdir -p /FinalPro/Worker
WORKDIR /FinalPro/Worker

COPY . .

#install all the reqvierment 
RUN pip3 install --user --upgrade -r src/requirements.txt --use-deprecated=legacy-resolver

ENV PYTHONPATH /FinalPro/Worker

#run the celery worker 
CMD ["/bin/sh", "-c","sudo celery -A FinalProject.CeleryWorkerTask worker -Q test --concurrency=1"]
