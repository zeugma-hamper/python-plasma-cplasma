#!/bin/bash

BOOST_VER=1.49.0
BOOST_DIR="boost_${BOOST_VER//./_}"

if ! [ -d "$BOOST_DIR" ]; then
    tar -xf "$BOOST_DIR.tar.gz"
fi
cd "$BOOST_DIR"
./bootstrap.sh --with-libraries=python

cat <<JAM > py27-config.jam
# Specify Python configuration
using python 
    : 2.7                       # Version of Python
    : /usr/bin/python2.7        # Path to the Python interpreter
    : /usr/include/python2.7    # Path to the Python headers
    : /usr/lib/x86_64-linux-gnu # Path to the Python libraries
    : <python-debugging>off     # No debugging symbols
    : <cxxflags>-std=c++11
    ;
JAM

# Install python boost library
sudo ./b2 install --with-python -sNO_BZIP2=1 --prefix=/usr --user-config=py27-config.jam -j$(nproc)
