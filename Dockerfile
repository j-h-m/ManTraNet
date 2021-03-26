FROM tensorflow/tensorflow:1.8.0-gpu

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y libgl1-mesa-glx

WORKDIR /usr/src/app

# install python 3.6
RUN apt-get install -y software-properties-common && \
        add-apt-repository ppa:deadsnakes/ppa && \
        apt-get update -y  && \
        apt-get install -y build-essential python3.6 python3.6-dev python3-pip && \
        apt-get install -y git  && \
        # update pip
        python3.6 -m pip install pip --upgrade && \
        python3.6 -m pip install wheel

# dev environment setup
COPY / .
RUN python3.6 -m pip install -r requirements.txt

# container main command
CMD jupyter notebook --ip 0.0.0.0 --port 8888 --no-browser --allow-root