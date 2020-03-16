#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_


from resources.uploads import UploadImg


def add_resource(api):
    api.add_resource(UploadImg, '/upload/image/')
