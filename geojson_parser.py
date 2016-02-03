#!/usr/bin/env python
# -*- coding: utf-8 -*
import io
import json

from lbs_helper import LbsHelper


def convert_geojson(source_file_name, target_file_name, convert_method):
    with open(source_file_name) as data_file:
        data_source = json.load(data_file)
        features = data_source.get('features')
        print('total {0} features'.format(len(features)))
        for feature in features:
            name = feature.get('properties').get('name').encode('utf-8')
            coordinates = feature.get('geometry').get('coordinates')
            geometry_type = feature.get('geometry').get('type')
            coordinates_size = 1
            if geometry_type == 'Point':
                feature.get('geometry')['coordinates'] = LbsHelper.convert_geojson_coordinate(coordinates,
                                                                                              convert_method)
            elif geometry_type == 'Polygon':
                coordinates_size = len(coordinates[0])
                coordinates_new = []
                for coordinate in coordinates[0]:
                    coordinates_new.append(LbsHelper.convert_geojson_coordinate(coordinate, convert_method))
                feature.get('geometry').get('coordinates')[0] = coordinates_new
            else:
                raise Exception('Unknown type: {0}'.format(geometry_type))
            print ('[{1}]{0} has {2} coordinates'.format(name, geometry_type, coordinates_size))
        with io.open(target_file_name, 'w', encoding='utf8') as outfile:
            data_write = json.dumps(data_source, ensure_ascii=False)
            outfile.write(unicode(data_write))


if __name__ == "__main__":
    # convert_geojson('zhouquan_wgs84.json','zhouquan_gcj02.json','wgs84_to_gcj02')
    # convert_geojson('wuzhong_gcj02_1.json', 'wuzhong_wgs84_1.json', 'gcj02_to_wgs84')
    # convert_geojson('data/wuzhong_area_wgs84.json', 'data/wuzhong_area_gcj02.json', 'wgs84_to_gcj02')
    convert_geojson('data/wuzhong_windturbine_wgs84.json', 'data/wuzhong_windturbine_gcj02.json', 'wgs84_to_gcj02')
