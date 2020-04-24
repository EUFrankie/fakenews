FROM ubuntu:latest

MAINTAINER Maurits De Roover "maurits-deroover@capveriant.com"

RUN apt-get update -y &&\
                apt-get install -y python3 python3-pip python3-dev &&\
                python3 -m pip install pip --upgrade

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 5000

ENTRYPOINT ["python3"]

CMD ["wsgi.py"]
