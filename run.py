#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_


from app import app, api
import resources
from resources import logging, accounts
from libs.auth import init_app
from config import LISTEN_ADDRESS, LISTEN_PORT, DEBUG

resources.add_resource(api)
init_app(app)
logging.add_resource(api)
accounts.add_resource(api)

if __name__ == '__main__':
    app.run(host=LISTEN_ADDRESS, port=LISTEN_PORT, debug=DEBUG)
