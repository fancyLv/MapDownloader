# -*- coding: utf-8 -*-
# @File    : google1.py
# @Author  : LVFANGFANG
# @Time    : 2018/7/7 0007 21:54
# @Desc    :

import math
import re
import requests


def deg2num(point, zoom):
    '''
    高德地图经纬度坐标(lng, lat)转瓦片坐标(tileX, tileY)
    :param point:
    :param zoom:
    :return:
    '''
    lat_rad = math.radians(point['lat'])
    n = 2.0 ** zoom
    tileX = int((point['lng'] + 180.0) / 360.0 * n)
    tileY = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (tileX, tileY)


def get_city_data(city):
    '''
    获取行政区划边界
    :param city:
    :return:
    '''
    url = 'https://restapi.amap.com/v3/config/district'

    params = {'subdistrict': '1',
              'extensions': 'all',
              'level': 'district',
              'key': '608d75903d29ad471362f8c58c550daf',
              's': 'rsv3',
              'output': 'json',
              'keywords': city,
              'platform': 'JS',
              'logversion': '2.0',
              'appname': 'https://lbs.amap.com/api/javascript-api/example/district-search/draw-district-boundaries/',
              'csid': 'EDF9F600-4CAE-4A1C-B9E5-DC7F85B474F1',
              'sdkversion': '1.4.6'}

    headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive',
               'Cookie': 'guid=c3ba-bf36-06f3-76d9; UM_distinctid=163c875d1572e-0b65f7f245e53d-5e4b2519-100200-163c875d1592c; cna=BobmEZlAaBgCAbcnxyuyvmb1; isg=BF9fYnoHeC0umHwwMLuLfchz7rMpbPRJxPtIu_Gs-45VgH8C-ZRDtt1yRlBbA4ve; key=608d75903d29ad471362f8c58c550daf',
               'Host': 'restapi.amap.com',
               'Referer': 'https://lbs.amap.com/api/javascript-api/example/district-search/draw-district-boundaries/',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'}

    r = requests.get(url, headers=headers, params=params)

    data = r.json()
    polyline = data['districts'][0]['polyline']
    # print(polyline)

    polyline_list = [i.split(',') for i in re.split(';|\|', polyline)]
    lng_list = [i[0] for i in polyline_list]
    lat_list = [i[1] for i in polyline_list]
    corner = {'lower_left_corner': {'lng': min(lng_list), 'lat': min(lat_list)},
              'upper_right_corner': {'lng': max(lng_list), 'lat': max(lat_list)}}

    return corner


if __name__ == '__main__':
    get_city_data('深圳市')
