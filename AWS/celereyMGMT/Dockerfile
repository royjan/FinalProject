
# load any public updates from python packages
FROM python:3

# upgrade any existing packages that can been updated
RUN apt-get -y upgrade

# make a directory for our application as our workdir
RUN mkdir -p /MGMT/FinalProject
WORKDIR /MGMT/FinalProject

COPY . .

#install all the reqvierment 
RUN pip3 install --user --upgrade -r src/requirements.txt --use-deprecated=legacy-resolver

ENV PYTHONPATH /MGMT/FinalProject

#exspose port 5000 for webserver 

EXPOSE 5000
#run the celery worker 
CMD ["/bin/sh", "-c","python3 src/main.py"]
