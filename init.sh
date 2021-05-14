#create the mgmt imag
sudo docker build -t celery_mgmt -f AWS/celereyMGMT/Dockerfile . ;
#create the worker img
sudo docker build -t celery_worker -f AWS/celereyWorker/Dockerfile . ;

# sudo docker run -i celery_mgmt -p 5000:5000/tcp

# sudo docker run -i celery_worker

#sudo docker system prune -a




