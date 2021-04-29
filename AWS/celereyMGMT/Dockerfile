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
RUN mkdir -p usr/src/MGMT/FinalProject
WORKDIR /usr/src/MGMT

#swap tp appuser
#USER celwork

COPY . ./FinalProject

#install all the reqvierment 
RUN pip3 install -r FinalProject/src/requirements.txt

#test
#RUN useradd --create-home celwork
#USER celwork

ENV PYTHONPATH "${PYTHONPATH}:/MGMT/FinalProject"

#exspose port 5000 for webserver 
EXPOSE 5000

#run the celery worker 
CMD ["python3", "FinalProject/src/main.py"]
