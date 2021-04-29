
# load any public updates from python packages
FROM python:3.8-slim-buster 

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# upgrade any existing packages that can been updated
RUN /opt/venv/bin/python3 -m pip install --upgrade pip

#added app user and setup
#RUN useradd --create-home celwork

# make a directory for our application as our workdir
RUN mkdir -p usr/src/Worker/FinalProject
WORKDIR /usr/src/Worker

COPY . ./FinalProject


#install all the reqvierment 
RUN pip3 install -r FinalProject/src/requirements.txt  

ENV PYTHONPATH "${PYTHONPATH}:/Worker/FinalProject"

#run the celery worker 
CMD ["python3", ,"celery -A FinalProject.CeleryWorkerTask worker -Q test --concurrency=1"]

#CMD ["/bin/sh", "-c","celery -A FinalProject.CeleryWorkerTask worker -Q test --concurrency=1"]
