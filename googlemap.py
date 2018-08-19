# -*- coding: utf-8 -*-
# @File    : googlemap.py
# @Author  : LVFANGFANG
# @Time    : 2018/7/7 0007 21:54
# @Desc    :

import math
import re

import requests


def deg2num(point, zoom):
    '''
    经纬度坐标(lng, lat)转瓦片坐标(tileX, tileY)
    :param point:
    :param zoom:
    :return:
    '''
    lat_rad = math.radians(point['lat'])
    n = 2.0 ** zoom
    tileX = int((point['lng'] + 180.0) / 360.0 * n)
    tileY = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (tileX, tileY)


def get_city_data(area):
    '''
    获取行政区划边界
    :param area:
    :return:
    '''
    areacode = area[1]
    url = 'https://restapi.amap.com/v3/config/district'
    params = {'subdistrict': '1',
              'showbiz': 'false',
              'extensions': 'all',
              'key': '608d75903d29ad471362f8c58c550daf',
              's': 'rsv3',
              'output': 'json',
              'level': 'district',
              'keywords': areacode,
              'platform': 'JS',
              'logversion': '2.0',
              'appname': 'https://lbs.amap.com/fn/iframe/?id=390&guide=1&litebar=4',
              'csid': 'CF806018-C80C-4875-A29E-1443A7C4B2BC',
              'sdkversion': '1.4.9'}
    headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive',
               'Host': 'restapi.amap.com',
               'Referer': 'https://lbs.amap.com/fn/iframe/?id=390&guide=1&litebar=4',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36', }
    r = requests.get(url, headers=headers, params=params, verify=False)
    data = r.json()
    if data['status'] == '1':
        polyline = data['districts'][0]['polyline']
        polyline_list = [i.split(',') for i in re.split(';|\|', polyline)]
        lng_list = [float(i[0]) for i in polyline_list]
        lat_list = [float(i[1]) for i in polyline_list]
        corner = {'lower_left_corner': {'lng': min(lng_list), 'lat': min(lat_list)},
                  'upper_right_corner': {'lng': max(lng_list), 'lat': max(lat_list)}}

        return corner


if __name__ == '__main__':
    print(get_city_data(('深圳市南山区', '440305')))
