#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_


from app import app, api
from resources import logging
from config import LISTEN_ADDRESS, LISTEN_PORT, DEBUG

logging.add_resource(api)

if __name__ == '__main__':
    app.run(host=LISTEN_ADDRESS, port=LISTEN_PORT, debug=DEBUG)
