# Final-Project-AWS

this reposetory contains all the AWS config , Docker and K8s files

# Building the Docker fild 
    #in 1st run there is a need to compile the difrent docker files 
    in the folder of ther requierd container run

    sudo docker build -t <CONTAINER_NAME> .
    
    _Note_:
    the container name are as the Folder name


    git checkout 0.4.0
    docker build -t quay.io/kubernetes-for-developers/celery-worker:0.4.0 .
    #git checkout master
    docker build -t quay.io/kubernetes-for-developers/celery-worker:latest .
    docker push quay.io/kubernetes-for-developers/celery-worker

# Running the Cluster
    kubectl run -i --tty \
    --image quay.io/kubernetes-for-developers/celery-worker:0.4.0 \
    --restart=Never --image-pull-policy=Always --rm testing /bin/sh


_Note_:
you will need to have previously invoked "docker login quay.io" to connect to
quay to send it images...

