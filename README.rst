===================================================================================
``Simple Uploader`` - Allow uploading of arbitrary files to the specific directory
===================================================================================

Dependencies
------------

- Based on the Python 3.6.0b3 released on October 31
- aiohttp version 1.1.5
- Simple jquery/fileinput plugin for frontend


Installation
------------

::

    docker build -t uploader .

Usage
-----

::

    docker run -p 8080:8080 -i -t uploader

Run tests
---------

::

    nose2

Notes
-----

::

    If there's a problem with openssl during pip install, try:
    env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" pip install cryptography