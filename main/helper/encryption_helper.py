#!/usr/bin/env python
#  -*- coding: utf-8 -*
from hashlib import md5, sha512
from random import Random


def generate_salt(length=8):
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    len_chars = len(chars) - 1
    random = Random()
    result = ''
    for i in range(length):
        # 每次从chars中随机取一位
        result += chars[random.randint(0, len_chars)]
    return result


def generate_md5(password, salt):
    md5_obj = md5()
    md5_obj.update(('%s%s' % (password, salt)).encode('utf-8'))
    return md5_obj.hexdigest()


def generate_md5_round(password, salt, encryption_round=1):
    cur_password = password
    for i in range(encryption_round):
        cur_password = generate_md5(cur_password, salt)
    return cur_password


def generate_sha512(password, salt):
    sha512_obj = sha512()
    sha512_obj.update(('%s%s' % (password, salt)).encode('utf-8'))
    return sha512_obj.hexdigest()
