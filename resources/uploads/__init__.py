#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_

import os
import sys
import datetime
import logging

from flask_restful import Resource, reqparse, request
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


# 目录不能以'/'开头
UPLOAD_PATH = 'static/images/'
ROOT_PATH = os.path.dirname(getattr(sys.modules['__main__'], '__file__'))


def get_path_and_filename(file_ext):
    now = datetime.datetime.now()
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    filename = '{}.{}'.format(str(datetime.datetime.now().timestamp()).split('.')[0], file_ext)
    full_path = os.path.join(ROOT_PATH, UPLOAD_PATH, year, month, day)
    os.makedirs(full_path, exist_ok=True)
    return os.path.join(full_path, filename)


def get_image_ext(filename):
    suffix = filename.rfind('.')
    if suffix == -1:
        raise Exception('图片格式不正确')
    file_ext = filename[suffix + 1:]
    if file_ext not in ['jpg', 'png', 'gif', 'bmp', 'jpeg', 'JPG', 'PNG',
                            'BMP', 'JPEG', ]:
        raise Exception('图片格式不正确')
    return file_ext


class UploadImg(Resource):
    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('image', type=FileStorage, location='files', required=True)
        img = parser.parse_args().get('image')
        try:
            filename = get_path_and_filename(get_image_ext(secure_filename(img.filename)))
            img.save(filename)
            file_url = '{}{}'.format(request.url_root, filename.split(ROOT_PATH)[1].lstrip('/'))
        except Exception as e:
            logging.error('上传图片失败, 错误: {}'.format(str(e.args)))
            return {"message": str(e.args)}
        return {'data': {'url': file_url}}

