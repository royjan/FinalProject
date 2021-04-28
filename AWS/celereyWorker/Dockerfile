
# load any public updates from python packages
FROM python:3

# upgrade any existing packages that can been updated
RUN apt-get -y upgrade

# make a directory for our application as our workdir
RUN mkdir -p /Worker/FinalProject
WORKDIR /Worker/FinalProject

COPY . .

#install all the reqvierment 
RUN pip3 -m install --no-cache-dir --upgrade pip

RUN pip3 -m install --user --upgrade -r src/requirements.txt --use-deprecated=legacy-resolver 

ENV PYTHONPATH "${PYTHONPATH}:/Worker/FinalProject"

#run the celery worker 
CMD ["/bin/sh", "-c","celery -A ../FinalProject.CeleryWorkerTask worker -Q test --concurrency=1"]
