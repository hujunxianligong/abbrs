# -*- coding: UTF-8 -*
import time
import config
from bin.jvm_crf_dic import SPCrf


def train_model(args, template_file_path=None, corpus_file_path=None, out_path=None,timestamp=None):
    if not timestamp:
        timestamp = config.TIMESTAMP
    if not template_file_path:
        template_file_path = config.CLASSSIFY_TEMPLATE_FILE
    if not corpus_file_path:
        corpus_file_path = config.CLASSSIFY_TRAIN_CORPUS_FILE
    if not out_path:
        out_path = ''.join([config.CLASSSIFY_MODEL_PATH, timestamp, '_crf_abbr_classify_model'])
    new_args = []
    if args:
        new_args.extend(args)
    new_args.extend([template_file_path, corpus_file_path, out_path])
    crf = SPCrf()
    crf.crf_learn(new_args)


if __name__ == '__main__':

    #options = ['-f', '1', '-c', '1']
    options = ['-h']
    train_model(options, template_file_path=None,
                corpus_file_path=None,#'/mnt/vol_0/wnd/usr/cmb_in/语料预处理结果/180516/1526327820_new_train_feature.crfpp'
                out_path=None)
