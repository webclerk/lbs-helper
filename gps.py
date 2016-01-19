#!/usr/bin/env python
# -*- coding: utf-8 -*


class Gps(object):
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def __str__(self):
        return '{0},{1}'.format(self.lat, self.lng)


if __name__ == "__main__":
    gps = Gps(30.58169, 120.34104)
    print gps

