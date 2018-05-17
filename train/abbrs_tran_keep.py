# -*- coding: UTF-8 -*
import time
import config
from bin.jvm_crf_dic import SPCrf


def train_model(args, template_file_path=None, corpus_file_path=None, out_path=None,timestamp=None):
    if not timestamp:
        timestamp = str(int(time.time()))
    if not template_file_path:
        template_file_path = config.ABBR_FEATURE_TEMPLATE
    if not corpus_file_path:
        corpus_file_path = config.ABBR_TRAIN_CORPUS_FILE
    if not out_path:
        out_path = ''.join([config.ABBR_TRAIN_MODEL_PATH, timestamp, '_crf_abbr_keep_model'])
    new_args = []
    if args:
        new_args.extend(args)
    new_args.extend([template_file_path, corpus_file_path, out_path])
    crf = SPCrf()
    crf.crf_learn(new_args)


if __name__ == '__main__':

    options = ['-f', '1', '-c', '1']
    train_model(options, template_file_path=None,
                corpus_file_path='/mnt/vol_0/wnd/usr/cmb_in/语料预处理结果/180516/1526327820_new_train_feature.crfpp',
                out_path=None)



