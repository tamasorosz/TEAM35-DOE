FROM ubuntu:20.04

# Set environment variables
ENV PYTHON_VERSION=3.8
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies and tools
RUN apt-get update && \
    apt-get install -y \
    python3-dev \
    libqt5xml5 \
    libqt5xmlpatterns5 \
    libqt5core5a \
    libumfpack5 \
    libmumps-seq-5.2.1 \
    libmetis5 \
    liblapack3 \
    libcurl4-gnutls-dev \
    gcc \
    g++ \
    curl  \
    xvfb \
    libx11-dev \
    libxrender-dev \
    libgl1-mesa-glx \
    libxt6 \
    mesa-utils \
    libgl1-mesa-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN Xvfb :99 -screen 0 1024x768x16 & export DISPLAY=:99
# Install specific version of Python
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update &&\
    apt-get install -y python${PYTHON_VERSION} python3-pip python3-matplotlib && \
    rm -rf /var/lib/apt/lists/*

ENV SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=True

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY src /app

VOLUME ["/app/output"]

#ENTRYPOINT ["python3.8", "team35_agros.py"]

ENTRYPOINT ["python3.8", "error_estimation.py"]