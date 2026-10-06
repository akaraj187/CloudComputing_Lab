# syntax=docker/dockerfile:1
# ------------------------------------------------------------------------------
# Experiment 2: Memory Performance Evaluation (VM vs Docker Container)
# Dockerfile for Sysbench Memory Benchmark Environment
# Base Image: Ubuntu 24.04 LTS (Noble Numbat)
# ------------------------------------------------------------------------------

FROM ubuntu:24.04

LABEL maintainer="Cloud Computing Lab"
LABEL description="Benchmark image equipped with Sysbench, FIO, iPerf3, and diagnostic utilities"

# Avoid interactive prompts during apt package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update repository metadata and install essential benchmark and diagnostic tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        sysbench \
        fio \
        iperf3 \
        python3 \
        python3-pip \
        procps \
        sysstat \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set up dedicated workspace for running benchmark workloads
WORKDIR /benchmark

# Default health/version check command
CMD ["sysbench", "--version"]
