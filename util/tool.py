# -*- coding: UTF-8 -*-
from urllib.parse import urlparse

import httplib2
import json


def read_dic(filepath=None, c_type=None):
    content = []
    if filepath:
        with open(filepath) as fp:
            while 1:
                lines = fp.readlines(100000)
                if not lines:
                    break
                for line in lines:
                    if line.startswith('#'):
                        continue
                    if not c_type:
                        content.append(line.strip('\n'))
                    else:
                        content.append((line.strip('\n'), c_type))
        if not c_type:
            content.sort(key=lambda x: len(x), reverse=True)
        else:
            content.sort(key=lambda x: len(x[0]), reverse=True)

    return content


class NLPDriver(object):
    head = {'connection': 'Keep-Alive',
            'Accept-Charset': 'utf-8',
            'Content-Type': 'application/x-www-form-urlencoded'}

    def __init__(self, url, timeout):
        r = urlparse(url)

        self.conn = httplib2.HTTPConnectionWithTimeout(host=r.hostname,
                                           port=r.port,
                                           timeout=timeout)
        self.url = url
        self.path = r.path

    def segment(self, param):
        self.conn.request('POST', self.path, param, NLPDriver.head)
        response = self.conn.getresponse()
        seg = {}

        if not response.status == 200:
            raise ValueError(response.status, response.reason)

        data = response.read()
        seg = json.loads(str(data, encoding='UTF-8'))
        return seg

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.close()
        else:
            print(exc_type, exc_val, exc_tb)
            return False
        return True