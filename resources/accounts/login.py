#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_


from flask_restful import Resource, reqparse
from collections import defaultdict
import time, datetime
from resources.accounts.models import User

login_limit = defaultdict(int)


class Login(Resource):

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('username', type=str, required=True, help="username is required", location='json')
        parse.add_argument('password', type=str, required=True, help="password is required", location='json')
        args = parse.parse_args()
        user = User.query.filter_by(name=args.get('username')).first()
        if user:
            if user.status:
                if user.verify_password(args.get('password')):
                    login_limit.pop(user.name, None)
                    user.access_token = user.generate_auth_token()
                    user.token_expired = time.time() + 8 * 60 * 60
                    user.last_time = user.login_time
                    user.login_time = datetime.datetime.now()
                    user.save()
                    return {
                        # "username": user.name,
                        # "cname": user.cname,
                        # "email": user.email,
                        # "is_super": user.is_super,
                        "access_token": user.access_token,
                        # "ctime": user.ctime.strftime('%Y-%m-%d %H:%M:%S'),
                        # "login_time": user.login_time.strftime('%Y-%m-%d %H:%M:%S'),
                        # "last_time": user.last_time.strftime('%Y-%m-%d %H:%M:%S'),
                        # "groups": [group.name for group in user.groups],
                        # "roles": [role.name for role in user.roles]
                    }
                else:
                    login_limit[user.name] += 1
                    if login_limit[user.name] >= 3:
                        user.update(status=False)
                    return {"message": "密码错误, 3次将被禁用, 当前次数: {}".format(login_limit[user.name])}, 401
            else:
                return {"message": "user {} is disabled!".format(user.name)}, 401
        elif login_limit[args.get('username')] >= 3:
            return {"message": "user {} is disabled!".format(args.get('username'))}, 401
        else:
            login_limit[args.get('username')] += 1
            return {"message": "用户名不存在"}, 401
