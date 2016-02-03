#!/usr/bin/env python
# -*- coding: utf-8 -*
import math

from gps import Gps


class LbsHelper(object):
    # 百度坐标系名称
    baidu_lbs_type = "bd09ll"
    a = 6378245.0
    ee = 0.00669342162296594323

    def __init__(self):
        pass

    @staticmethod
    def out_of_china(lat, lng):
        """
        是否在中国境内，这个是用了矩形的近似算法
        :param lat:
        :param lng:
        :return:
        """
        if lat > 55.8271 or lat < 0.8293:
            return True
        if lng > 137.8347 or lng < 72.004:
            return True
        return False

    @staticmethod
    def transform_lat(x, y):
        ret_lat = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
        ret_lat += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
        ret_lat += (20.0 * math.sin(y * math.pi) + 40.0 * math.sin(y / 3.0 * math.pi)) * 2.0 / 3.0
        ret_lat += (160.0 * math.sin(y / 12.0 * math.pi) + 320 * math.sin(y * math.pi / 30.0)) * 2.0 / 3.0
        return ret_lat

    @staticmethod
    def transform_lng(x, y):
        ret_lng = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
        ret_lng += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
        ret_lng += (20.0 * math.sin(x * math.pi) + 40.0 * math.sin(x / 3.0 * math.pi)) * 2.0 / 3.0
        ret_lng += (150.0 * math.sin(x / 12.0 * math.pi) + 300.0 * math.sin(x / 30.0 * math.pi)) * 2.0 / 3.0
        return ret_lng

    @staticmethod
    def transform(lat, lng):
        # 暂时不考虑是否在中国境内的问题
        # if LbsHelper.out_of_china(lat, lng):
        #     return Non
        d_lat = LbsHelper.transform_lat(lng - 105.0, lat - 35.0)
        d_lng = LbsHelper.transform_lng(lng - 105.0, lat - 35.0)
        rad_lat = lat / 180.0 * math.pi
        magic = math.sin(rad_lat)
        magic = 1 - LbsHelper.ee * magic * magic
        sqrt_magic = math.sqrt(magic)
        d_lat = (d_lat * 180.0) / ((LbsHelper.a * (1 - LbsHelper.ee)) / (magic * sqrt_magic) * math.pi)
        d_lng = (d_lng * 180.0) / (LbsHelper.a / sqrt_magic * math.cos(rad_lat) * math.pi)
        mg_lat = lat + d_lat
        mg_lng = lng + d_lng
        return Gps(mg_lat, mg_lng)

    @staticmethod
    def wgs84_to_gcj02(lat, lng):
        """
        将wgs84转化为火星坐标系
        :param lat:
        :param lng:
        :return:
        """
        # 暂时不考虑是否在中国境内的问题
        # if LbsHelper.out_of_china(lat, lng):
        #     return None
        d_lat = LbsHelper.transform_lat(lng - 105.0, lat - 35.0)
        d_lng = LbsHelper.transform_lng(lng - 105.0, lat - 35.0)
        rad_lat = lat / 180.0 * math.pi
        magic = math.sin(rad_lat)
        magic = 1 - LbsHelper.ee * magic * magic
        sqrt_magic = math.sqrt(magic)
        d_lat = (d_lat * 180.0) / ((LbsHelper.a * (1 - LbsHelper.ee)) / (magic * sqrt_magic) * math.pi)
        d_lng = (d_lng * 180.0) / (LbsHelper.a / sqrt_magic * math.cos(rad_lat) * math.pi)
        mg_lat = lat + d_lat
        mg_lng = lng + d_lng
        return Gps(mg_lat, mg_lng)

    @staticmethod
    def gcj02_to_wgs84(lat, lng):
        """
        火星坐标系转换为WGS84
        :param lat:
        :param lng:
        :return:
        """
        gps = LbsHelper.transform(lat, lng)
        res_lat = lat * 2 - gps.lat
        res_lng = lng * 2 - gps.lng
        return Gps(res_lat, res_lng)

    @staticmethod
    def gcj02_to_bd09(gcj_lat, gcj_lng):
        """
        将火星坐标系转换为百度坐标系
        :param gcj_lat:
        :param gcj_lng:
        :return:
        """
        x = gcj_lng
        y = gcj_lat
        z = math.sqrt(x * x + y * y) + 0.00002 * math.sin(y * math.pi)
        theta = math.atan2(y, x) + 0.000003 * math.cos(x * math.pi)
        bd_lng = z * math.cos(theta) + 0.0065
        bd_lat = z * math.sin(theta) + 0.006
        return Gps(bd_lat, bd_lng)

    @staticmethod
    def bd09_to_gcj02(bd_lat, bd_lng):
        """
        将百度坐标系转换为火星坐标系
        :param bd_lat:
        :param bd_lng:
        :return:
        """
        x = bd_lng - 0.0065
        y = bd_lat - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * math.pi)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * math.pi)
        gcj_lng = z * math.cos(theta)
        gcj_lat = z * math.sin(theta)
        return Gps(gcj_lat, gcj_lng)

    @staticmethod
    def bd09_to_wgs84(bd_lat, bd_lng):
        gps_gcj02 = LbsHelper.bd09_to_gcj02(bd_lat, bd_lng)
        return LbsHelper.gcj02_to_wgs84(gps_gcj02.lat, gps_gcj02.lng)

    @staticmethod
    def convert_geojson_coordinate(coordinate, convert_method):
        """
        将GEOJSON的坐标点进行转换
        :param coordinate:
        :param convert_method:
        :return:
        """
        lng = coordinate[0]
        lat = coordinate[1]
        alt = coordinate[2]
        # print('old coordinate: {0}'.format(coordinate))
        if convert_method == 'wgs84_to_gcj02':
            gps_gcj = LbsHelper.wgs84_to_gcj02(lat, lng)
            return [gps_gcj.lng, gps_gcj.lat, alt]
        elif convert_method == 'gcj02_to_wgs84':
            gps_wgs = LbsHelper.gcj02_to_wgs84(lat, lng)
            return [gps_wgs.lng, gps_wgs.lat, alt]
        else:
            raise Exception('Not matched convert method')
            # return [coordinate.lng, coordinate.lat, coordinate.alt]

if __name__ == "__main__":
    gps_wgs_test = Gps(30.58169, 120.34104)
    print LbsHelper.wgs84_to_gcj02(gps_wgs_test.lat, gps_wgs_test.lng)
