FROM python:3

WORKDIR /usr/src/worker/FinalProject

COPY requirements.txt ./

RUN pip3 install -r requirements.txt --use-deprecated=legacy-resolver

COPY . . 

ENV PYTHONPATH /usr/src/worker/FinalProject

CMD [ "python3", "main.py" ]
