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
    gcc \
    g++ \
    curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Install specific version of Python
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update &&\
    apt-get install -y python${PYTHON_VERSION} python3-pip && \
    rm -rf /var/lib/apt/lists/*
