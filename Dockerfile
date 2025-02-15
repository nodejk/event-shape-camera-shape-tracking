FROM python:3.10.10-bullseye
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y
RUN apt-get install curl -y
RUN apt-get install sudo -y

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /event-camera

COPY ./ ./

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

# CMD ["/usr/bin/python3", "main.py"]
CMD ["sleep", "infinity"]
