# -*- coding: UTF-8 -*
import os
import time
import config
from bin.jvm_crf_dic import crf_learn
from util.tool import get_closest_file


def train_model(args, template_file_path=None, corpus_file_path=None, out_path=None,timestamp=None):
    if not timestamp:
        timestamp = str(int(time.time()))
    if not template_file_path:
        template_file_path = config.ABBR_FEATURE_TEMPLATE
    if not corpus_file_path:
        corpus_file_path = config.ABBR_TRAIN_CORPUS_FILE
        if not os.path.exists(corpus_file_path):
            corpus_file_path = get_closest_file(config.ABBR_PRE_RE_PATH, '_new_train_feature.crfpp')
    if not out_path:
        out_path = ''.join([config.ABBR_TRAIN_MODEL_PATH, timestamp, '_crf_abbr_keep_model'])
    new_args = []
    if args:
        new_args.extend(args)
    new_args.extend([template_file_path, corpus_file_path, out_path])
    crf_learn(new_args)


if __name__ == '__main__':

    options = ['-f', '1', '-c', '1']
    train_model(options, template_file_path=None,
                corpus_file_path=None,
                out_path=None)



