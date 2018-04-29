# -*- coding: UTF-8 -*-

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
    content.sort(key=lambda x: len(x))
    content.reverse()

    return content
