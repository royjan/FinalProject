# Final-Project-AWS

this reposetory contains all the AWS config , Docker and K8s files

## 

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

