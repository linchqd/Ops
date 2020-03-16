#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_


import os
import logging
from logging.config import dictConfig
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
import config


# logging setting
class LogFilter(logging.Filter):
    def filter(self, record):
        if record.levelno > 30:
            return False
        return True


log_dir = os.path.join(os.path.dirname(os.path.abspath(__name__)), 'logs/')

os.makedirs(log_dir, exist_ok=True)

dictConfig({
    'version': 1,
    'formatters': {
        'access': {
            'format': '%(asctime)s %(levelname)s: %(message)s'
        },
        'error': {
            'format': '%(asctime)s %(levelname)s: %(filename)s:%(module)s:%(funcName)s:%(lineno)d:%(message)s'
        }
    },
    'handlers': {
        'access': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'INFO',
            'filename': '{}access.log'.format(log_dir),
            'when': 'D',
            'interval': 1,
            'backupCount': 7,
            'encoding': 'utf-8',
            'formatter': 'access',
            'filters': ['access']
        },
        'error': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'ERROR',
            'filename': '{}error.log'.format(log_dir),
            'when': 'D',
            'interval': 1,
            'backupCount': 7,
            'encoding': 'utf-8',
            'formatter': 'error'
        }
    },
    'filters': {
        'access': {
            '()': LogFilter
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['access', 'error']
    }
})

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
