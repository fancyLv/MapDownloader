# -*- coding: utf-8 -*-
# @File    : location.py
# @Author  : LVFANGFANG
# @Time    : 2018/4/22 0022 0:53
# @Desc    :

import re

import requests


def get_jsonData(url):
    headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive',
               'Host': 'map.baidu.com',
               'Referer': 'https://map.baidu.com/',
               'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
    req = requests.get(url, headers=headers)
    data = req.json()
    return data


def get_uid(city):
    url = "http://map.baidu.com/?newmap=1&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=s&wd=%s&nn=0&ie=utf-8" % city
    data = get_jsonData(url)
    uid = data.get('content').get('uid')
    return uid


def get_boundaries(city):
    uid = get_uid(city)
    url = 'http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=ext&num=1000&l=10&uid=%s&tn=B_NORMAL_MAP&nn=0&ie=utf-8' % uid
    boundaries = {}
    data = get_jsonData(url)
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

        return boundaries


if __name__ == '__main__':
    boundaries = get_boundaries(u'广东省')
    boundary = boundaries['boundary']
