
# load any public updates from python packages
FROM python:3

# upgrade any existing packages that can been updated
RUN apt-get -y upgrade

# make a directory for our application as our workdir
RUN mkdir -p /FinalPro/MGMT
WORKDIR /FinalPro/MGMT

COPY . .

#install all the reqvierment 
RUN pip3 install --user --upgrade -r requirements.txt --use-deprecated=legacy-resolver

ENV PYTHONPATH /FinalPro/MGMT
#run the celery worker 
CMD ["/bin/sh", "-c","python3 src/main.py"]
