#!/usr/bin/env python
# -*- coding: utf-8 -*
import json

from lbs_helper import LbsHelper

with open('zhouquan_wgs84.json') as data_file:
    data_wgs84 = json.load(data_file)
    features = data_wgs84.get('features')
    print('total {0} features'.format(len(features)))
    for feature in features:
        coordinates = feature.get('geometry').get('coordinates')[0]
        print('total {0} coordinates'.format(len(coordinates)))
        coordinates_new = []
        for coordinate in coordinates:
            lng = coordinate[0]
            lat = coordinate[1]
            alt = coordinate[2]
            gps_gcj = LbsHelper.wgs84_to_gcj02(lat, lng)
            # print('old coordinate: {0}'.format(coordinate))
            coordinate_new = [gps_gcj.lng, gps_gcj.lat, alt]
            coordinates_new.append(coordinate_new)
            # print('new coordinate: {0}'.format(coordinate))
            # data = f.read()
        feature.get('geometry').get('coordinates')[0] = coordinates_new
    with open('zhouquan_gcj.json', 'w') as outfile:
        json.dump(data_wgs84, outfile)
