#!/usr/bin/env python
#  -*- coding: utf-8 -*
import os.path
import zlib
from datetime import datetime, date
from decimal import Decimal
from enum import Enum
import arrow
import simplejson as json


def build_current_path_by_file(related_file, file_name):
    cur_path = os.path.dirname(os.path.abspath(related_file))
    return os.path.join(cur_path, file_name)


def load_options(current_options, loaded_options=None, append_not_existed_key=False):
    """
    对于当前选项通过加载的选项进行补充
    :param current_options: 当前选项
    :param loaded_options: 加载的选项
    :param append_not_existed_key: 只处理在当前选项中已存在的键
    :return:
    """
    if loaded_options:
        for option_key in loaded_options:
            if append_not_existed_key:
                current_options[option_key] = loaded_options[option_key]
            elif option_key in current_options:
                current_options[option_key] = loaded_options[option_key]


def datetime_utc_to_local(datetime_utc):
    """
    UTC时间转本地时间
    :param datetime_utc: utc datetime
    :return:
    """
    return arrow.Arrow.fromdatetime(datetime_utc).datetime.astimezone()


def datetime_local_to_utc(datetime_local):
    """
    本地时间转UTC时间
    :param datetime_local: 本地datetime
    :return:
    """
    return arrow.Arrow.fromdatetime(datetime_local).to('utc')


def utc_timestamp_to_local_datetime(input_timestamp):
    """
    将时间戳转换为本地时间
    :param input_timestamp:
    :return:
    """
    return arrow.Arrow.utcfromtimestamp(input_timestamp).datetime.astimezone()


def datetime_to_utc_timestamp(input_time):
    """
    将datetime数据对象转换为Unix timestamp，为整数
    :param input_time:
    :return:
    """
    return arrow.Arrow.fromdatetime(input_time).to('utc').timestamp


def string_to_local_datetime(datetime_str):
    """
    根据字符串转化为时间，作为本地时间
    :param datetime_str: 时间的字符串表达 %Y-%m-%d %H:%M:%S, 秒后面的数据会被丢弃掉
    :return: 本地的datetime
    """
    dt_obj = datetime.strptime(datetime_str[:18], '%Y-%m-%d %H:%M:%S')
    return dt_obj.astimezone()


def zlib_compress(string_data, level=1):
    """
    将文本数据进行zlib压缩
    :param string_data:
    :param level:压缩级别，1-9
    :return:
    """
    return zlib.compress(string_data.encode('utf-8'), level)


def zlib_decompress(byte_data):
    """
    将二进制数据进行zlib解压缩
    :param byte_data:
    :return:
    """
    return zlib.decompress(byte_data).decode('utf-8')


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        # print(type(obj))
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, (datetime, date)):
            obj_utc = datetime_local_to_utc(obj.astimezone())
            return datetime_to_utc_timestamp(obj_utc)
            # return obj.strftime('%Y-%m-%d %H:%M:%S')
            # return obj.isoformat()
        return json.JSONEncoder.default(self, obj)
