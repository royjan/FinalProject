#create the mgmt imag
sudo docker build -t celery_mgmt -f AWS/celereyMGMT/Dockerfile . ;
#create the worker img
sudo docker build -t celery_worker -f AWS/celereyWorker/Dockerfile . ;