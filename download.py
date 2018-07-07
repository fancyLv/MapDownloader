# -*- coding: utf-8 -*-
# @File    : download.py
# @Author  : LVFANGFANG
# @Time    : 2018/6/7 0007 15:21
# @Desc    :

import random
import math
import os
import queue
import time

import requests
from PyQt5.QtCore import QThread, pyqtSignal

from location import get_boundaries


class ImageDownloadThread(QThread):
    sub_progressBar_updated_signal = pyqtSignal()

    def __init__(self, task_q, path, style=None):
        super(ImageDownloadThread, self).__init__()
        self.running = True
        self.stopped = False
        self.task_q = task_q
        self.path = path
        self.style = style
        self.start()

    def __del__(self):
        self.wait()

    def stop(self):
        self.stopped = True

    def pause(self):
        if self.isRunning():
            self.running = not self.running

    def run(self):
        url = 'http://api{}.map.bdimg.com/customimage/tile'.format(random.choice(range(3)))
        while True:
            if self.running:
                try:
                    x, y, z = self.task_q.get_nowait()
                except queue.Empty as e:
                    break
                data = {'x': x,
                        'y': y,
                        'z': z,
                        'udt': '20180608',
                        'scale': '1',
                        'ak': 'E4805d16520de693a3fe707cdc962045'}
                if self.style:
                    data.update({'styles': self.style})
                os.makedirs(os.path.join(self.path, 'tiles', str(z), str(x)), exist_ok=True)
                while True:
                    try:
                        r = requests.get(url, params=data)
                        filename = os.path.join(self.path, 'tiles', str(z), str(x), '{}.jpg'.format(y))
                        with open(filename, 'wb') as f:
                            f.write(r.content)
                        break
                    except Exception as e:
                        print(repr(e))
                        time.sleep(3)
                self.sub_progressBar_updated_signal.emit()
            if self.stopped:
                break


class DownloadEngine(QThread):
    division_done_signal = pyqtSignal(int)
    download_done_signal = pyqtSignal()
    progressBar_updated_signal = pyqtSignal()

    def __init__(self, area, zoom_list, path, style, thread_num):
        super(DownloadEngine, self).__init__()
        self.area = area
        self.zoom_list = zoom_list
        self.path = os.path.join(path, area)
        self.style = style
        self.thread_num = int(thread_num)

    def __del__(self):
        self.wait()

    def pause(self):
        if self.isRunning():
            for t in self.threads:
                t.pause()

    def get_task_queue(self):
        task_q = queue.Queue()
        boundaries = get_boundaries(self.area)
        corner = boundaries['corner']

        for z in self.zoom_list:
            z = int(z)
            x1 = math.floor(corner['lower_left_corner']['lng'] / math.pow(2, 18 - z) / 256)
            y1 = math.floor(corner['lower_left_corner']['lat'] / math.pow(2, 18 - z) / 256)
            x2 = math.ceil(corner['upper_right_corner']['lng'] / math.pow(2, 18 - z) / 256)
            y2 = math.ceil(corner['upper_right_corner']['lat'] / math.pow(2, 18 - z) / 256)

            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    task_q.put((x, y, z))
        return task_q

    def sub_update_progressBar(self):
        self.progressBar_updated_signal.emit()

    def run(self):
        task_q = self.get_task_queue()
        self.threads = []
        self.division_done_signal.emit(task_q.qsize())
        for i in range(self.thread_num):
            thread = ImageDownloadThread(task_q, self.path, self.style)
            thread.sub_progressBar_updated_signal.connect(self.sub_update_progressBar)
            self.threads.append(thread)
        for thread in self.threads:
            thread.wait()
        self.download_done_signal.emit()

    def terminate(self):
        for t in self.threads:
            t.terminate()
        self.threads = []
        super(DownloadEngine, self).terminate()
