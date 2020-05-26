FROM ubuntu:latest

MAINTAINER Maurits De Roover "maurits-deroover@capveriant.com"

RUN apt-get update -y &&\
                apt-get install -y python3 python3-pip python3-dev &&\
                python3 -m pip install pip --upgrade

RUN apt-get install -y git

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

# If the trained model is already available locally it should 
# be copied as well and this file doesn't do anything.
RUN python3 download_encoder_model.py 

EXPOSE 5000

ENTRYPOINT ["python3"]

CMD ["wsgi.py"]
