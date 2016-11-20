===================================================================================
``Simple Uploader`` - Allow uploading of arbitrary files to the specific directory
===================================================================================

.. image:: https://img.shields.io/travis/bndr/basic-uploader.svg
        :target: https://travis-ci.org/bndr/basic-uploader

Dependencies
------------

- Based on the Python 3.6.0b3 released on October 31
- aiohttp version 1.1.5
- Simple jquery/fileinput plugin for frontend


Installation
------------

::

    git clone git@github.com:bndr/basic-uploader.git && cd basic-uploader
    docker build -t uploader .

Usage
-----

::

    python run.py
    OR
    docker run -p 8080:8080 -i -t uploader

Run tests
---------

::

    nose2

Endpoints
------------

- GET / - Root endpoints, file uploader form
- GET /list/ - List all uploaded files
- GET /api/v1/download/<filename> - Download the specified file if it exists
- POST /api/v1/upload/ - Upload file

Notes
-----

::

    If there's a problem with openssl during pip install, try:
    env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" pip install cryptography