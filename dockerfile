FROM conda/miniconda3
WORKDIR /usr/src/Olis_cleaningApp
COPY ./ ./

SHELL ["/bin/sh", "-c"]

RUN conda env create -n olis_cleaning -f environment.yml

# check for conda info and python info
RUN conda activate olis-cleaning && conda info && python --version

# test to see if all the libraries are available
RUN conda activate olis-cleaning && pythin test.py && echo "all libraries available"