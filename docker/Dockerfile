FROM plasma

RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update
RUN apt-get install -y \
    python2.7 \
    python2.7-dev \
    python-pip

RUN pip2 install wheel
RUN pip2 install numpy

RUN ln -s /usr/bin/python2.7 /usr/bin/python

COPY boost_1_49_0.tar.gz install_boost.sh /opt/boost/
WORKDIR /opt/boost/
RUN ./install_boost.sh
