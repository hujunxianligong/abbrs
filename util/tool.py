# -*- coding: UTF-8 -*-

def read_dic(filePath=None,type=None):
    content = []
    if filePath:
        with open(filePath) as fp:
            while 1:
                lines = fp.readlines(100000)
                if not lines:
                    break
                for line in lines:
                    if line.startswith('#'):
                        continue
                    if not type:
                        content.append(line.strip('\n'))
                    else:
                        content.append((line.strip('\n'),type))
        if not type:
            content.sort(key=lambda x: len(x),reverse=True)
        else:
            content.sort(key=lambda x : len(x[0]),reverse=True)

    return content
