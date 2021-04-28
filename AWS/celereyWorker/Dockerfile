
# load any public updates from python packages
FROM python:3

# upgrade any existing packages that can been updated
RUN apt-get -y upgrade

# make a directory for our application as our workdir
RUN mkdir -p usr/src/Worker/FinalProject
WORKDIR /usr/src/Worker

COPY . .

#install all the reqvierment 
RUN pip3 install -r src/requirements.txt --use-deprecated=legacy-resolver 

ENV PYTHONPATH "${PYTHONPATH}:/Worker/FinalProject"

#run the celery worker 
CMD ["python3", ,"celery -A FinalProject.CeleryWorkerTask worker -Q test --concurrency=1"]

#CMD ["/bin/sh", "-c","celery -A FinalProject.CeleryWorkerTask worker -Q test --concurrency=1"]
