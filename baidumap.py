# -*- coding: utf-8 -*-
# @File    : baidumap.py
# @Author  : LVFANGFANG
# @Time    : 2018/4/22 0022 0:53
# @Desc    :

import re

import requests


def get_jsonData(url, params):
    headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive',
               'Host': 'map.baidu.com',
               'Referer': 'https://map.baidu.com/',
               'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
    req = requests.get(url, headers=headers, params=params, verify=False)
    data = req.json()
    return data


def get_uid(city):
    url = 'http://map.baidu.com/'
    params = {'newmap': '1',
              'biz': '1',
              'from': 'webmap',
              'da_par': 'direct',
              'pcevaname': 'pc4.1',
              'qt': 's',
              'wd': city,
              'nn': '0',
              'ie': 'utf-8'}
    data = get_jsonData(url, params)
    uid = data.get('content').get('uid')
    return uid


def get_city_data(area):
    '''
    获取行政区划边界
    :param area:
    :return:
    '''
    city = area[0]
    uid = get_uid(city)
    url = 'http://map.baidu.com/'
    boundaries = {}
    params = {'newmap': '1',
              'reqflag': 'pcmap',
              'biz': '1',
              'from': 'webmap',
              'da_par': 'direct',
              'pcevaname': 'pc4.1',
              'qt': 'ext',
              'num': '1000',
              'l': '10',
              'uid': uid,
              'tn': 'B_NORMAL_MAP',
              'nn': '0',
              'ie': 'utf-8'}
    data = get_jsonData(url, params)
    content = data.get('content')
    if content:
        geo = content['geo']
        location = geo.split('|')
        corners = location[1].split(';')
        corner = {}
        corner['lower_left_corner'] = {'lng': float(corners[0].split(',')[0]), 'lat': float(corners[0].split(',')[1])}
        corner['upper_right_corner'] = {'lng': float(corners[1].split(',')[0]), 'lat': float(corners[1].split(',')[1])}

        boundary = re.split('[,;]', location[2].strip(';'))
        points = []
        for i in range(0, len(boundary) - 2, 2):
            point = {'lng': float(boundary[i]), 'lat': float(boundary[i + 1])}
            points.append(point)

        boundaries['corner'] = corner
        boundaries['boundary'] = points

        return boundaries['corner']


def point2num(point, zoom):
    '''
    墨卡托坐标(pointX, pointY)转瓦片坐标(tileX, tileY)
    :param point:
    :param zoom:
    :return:
    '''
    tileX = int(point['lng'] / 2 ** (18 - zoom) / 256)
    tileY = int(point['lat'] / 2 ** (18 - zoom) / 256)
    return (tileX, tileY)


if __name__ == '__main__':
    boundaries = get_city_data(u'广东省')
    boundary = boundaries['boundary']
