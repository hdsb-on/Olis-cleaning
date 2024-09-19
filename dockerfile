FROM continuumio/miniconda3
WORKDIR /usr/src/Olis_cleaningApp
COPY ./ ./

SHELL ["/bin/bash","-l", "-c"]

# initialize env from config file
RUN conda env create -n olis_cleaning -f environment.yml

# generate config files for bash
RUN conda init bash

# automatically activate the environment
RUN echo "conda activate olis_cleaning" >> ~/.bashrc

# set entrypoint to bash
ENTRYPOINT ["bash", "-l", "-c"]