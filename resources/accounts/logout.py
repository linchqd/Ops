#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_


from flask_restful import Resource
from flask import g


class Logout(Resource):

    @staticmethod
    def post():
        g.user.token_expired = 0
        g.user.save()
        return {}
