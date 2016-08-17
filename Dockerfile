FROM ubuntu:14.04

MAINTAINER Sam Coles <sam.coles@giantquanta.com>

RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
      curl \
      libfreetype6-dev \
      libpng12-dev \
      libzmq3-dev \
      pkg-config \
      python \
      python-dev \
      python-numpy \
      python-pip \
      python-scipy \
      rsync \
      unzip \
      && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -O https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    rm get-pip.py

RUN pip --no-cache-dir install \
        ipykernel \
        jupyter \
        matplotlib \
        websocket-client \
        pandas \
        && python -m ipykernel.kernelspec

ENV TENSORFLOW_VERSION 0.10.0rc0

RUN pip --no-cache-dir install \
    http://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-${TENSORFLOW_VERSION}-cp27-none-linux_x86_64.whl

COPY jupyter_notebook_config.py /root/.jupyter/

COPY run_jupyter.sh /

COPY notebooks /notebooks

COPY python /python_libs

ENV PYTHONPATH $PYTHONPATH:/python_libs

# TensorBoard
EXPOSE 6006
# IPython
EXPOSE 8888

WORKDIR "/notebooks"

CMD ["/run_jupyter.sh"]
