FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y sudo \
    build-essential \
    curl \
    libcurl4-openssl-dev \
    libssl-dev \
    wget \
    python3-dev \
    python3-pip \
    libxrender-dev \
    libxext6 \
    libsm6 \
    openssl
    
RUN mkdir -p /opt/timeline

COPY data /opt/timeline/data
COPY model /opt/timeline/model
COPY src /opt/timeline/src
COPY requirements.txt /opt/timeline

WORKDIR /opt/timeline

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 8501