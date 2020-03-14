#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_


from flask_restful import Resource


def add_resource(api):
    api.add_resource(Logging, '/logging/')


class Logging(Resource):
    pass
