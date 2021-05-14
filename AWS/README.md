# Final-Project-AWS

    this sub-repo contains all the config for AWS for the grid-scale project

# Building the Docker fild 
    #in 1st run there is a need to compile the difrent docker files 
    #in the folder of ther requierd container run

    sudo docker build -t <CONTAINER_NAME> .
    
    for exmple 
    #create the mgmt imag
    sudo docker build -t celery_mgmt -f AWS/celereyMGMT/Dockerfile . 
#   create the worker img
    sudo docker build -t celery_worker -f AWS/celereyWorker/Dockerfile . 

#   running the dockers 
    # sudo docker run -i celery_mgmt -p 5000:5000/tcp

    # sudo docker run -i celery_worker


    #clean command , will delete all docker related config on your system (used to clean ceche befoure instance termination)
    #sudo docker system prune -a


# Running the Cluster
    kubectl apply -f FinalProject\AWS\deploy\deployment.yml


_Note_:
you will need to have previously invoked "docker login quay.io" to connect to
quay to send it images...

