# -*- coding: UTF-8 -*-
from pyhanlp import *

def read_dic(filePath=None):
    content = []
    with open(filePath) as fp:
        while 1:
            lines = fp.readlines(100000)
            if not lines:
                break
            for line in lines:
                if line.startswith('#'):
                    continue
                content.append(line.strip('\n'))
    sorted(content,key=lambda x: len(x))

    return content

class Seg_han():
    def __init__(self):
        SafeJClass('com.hankcs.hanlp.utility.Predefine').HANLP_PROPERTIES_PATH = '/mnt/vol_0/wnd/usr/workspace/cmb/model/hanlp.properties'
        for term in HanLP.segment('其中流贷为'):
            print('{}\t{}'.format(term.word, term.nature))  # 获取单词与词性
if __name__ == "__main__":
    test =Seg_han()