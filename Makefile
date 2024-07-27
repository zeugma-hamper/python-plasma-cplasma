
SETUP_FLAGS = G_SPEAK_HOME=/usr APPLY_LP2002043_UBUNTU_CFLAGS_WORKAROUND=1
BOOST_SRC = "docker/boost_1_49_0.tar.gz"
BOOST_URL = "http://sourceforge.net/projects/boost/files/boost/1.49.0/boost_1_49_0.tar.gz"

.PHONY: test shell

all: test-docker

test-docker: docker
	docker run -ti --rm -v $$PWD:/work -w /work cplasma /bin/bash -c 'make test'

test:
	${SETUP_FLAGS} python setup.py build_ext --inplace
	python test/yamlio_test.py
	python test/pool_server_test.py
	python test/unicode_test.py
	python test/hash_test.py
	python test/test_readable_slaw.py

shell: docker
	docker run --name cplasma-shell -ti --rm -v $$PWD:/work -w /work cplasma /bin/bash

docker: docker/Dockerfile ${BOOST_SRC}
	docker build -f docker/Dockerfile docker/ -t cplasma

# Download Boost from this link https://www.boost.org/users/history/version_1_49_0.html
${BOOST_SRC}:
	test -f $@ || wget ${BOOST_URL} -O ${BOOST_SRC}
