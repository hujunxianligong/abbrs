# -*- coding: UTF-8 -*-
import argparse
import os

import config
import re
from flask import Flask
from flask import request
from load.load_model import get_model_abbr
import config as sys_config
from logger_manager import seg_api_logger as logger
from preprocessor.corpus_classify_train import Pretreatment
from train.classify_train_model import train_model

app = Flask(__name__)


@app.route('/api/abbner', methods=['POST'])
def abb_classify():
    data = request.data
    if data == b'':
        data = dict(request.form)
        for key in data:
            data = key
            break
        print(data)
        data = re.sub('[\(（）\)]', '', data)
    else:
        data = re.sub('[\(（）\)]', '', data.decode('UTF-8'))
    logger.info(G)
    result = get_model_abbr(data, G)
    json = result.set_api_json()
    del result
    return json


def save_pid(path, pid):
    with open(path, 'w') as fp:
        fp.write(str(pid))


def run():
    try:
        port = G.seg_port
    except ValueError and IndexError and AttributeError:
        port = 5007

    try:
        app.run(debug=sys_config.DEBUG, host='0.0.0.0', port=port, threaded=False)
    except Exception as e:
        print(e)


def detach_proc(func, pid_file):
    pid = os.fork()
    if pid == 0:
        func()
    else:
        # saved PID of child process
        logger.info('Daemon process detached at PID: ' + str(pid))
        save_pid(pid_file, pid)

G = None
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Abbreviation node API.')
    subparsers = parser.add_subparsers(help='sub-command help')

    reg_parser = subparsers.add_parser('load_seg', help='load abbreviation Segmentation model to serve')
    reg_parser.add_argument('--path', dest='load_model_path', help='Select the location of the model',
                            default=config.CLASSSIFY_MODEL_FILE)
    reg_parser.add_argument('--port', dest='seg_port', type=int, default=config.SEG_API_PORT, help='API serve port')
    reg_parser.add_argument('--pid', dest='seg_pid', default=config.SEG_API_PID_FILE, help='pid path', metavar='PID_FILE')
    reg_parser.add_argument('--detach', action='store_true', help='running background')
    reg_parser.set_defaults(mode='load_seg')

    dam_parser = subparsers.add_parser('build_seg', help='Construction abbreviation classification training set')
    dam_parser.add_argument('--inType',  dest='in_Type', help='input data method,meaning : mysql/file', default='file')
    dam_parser.add_argument('--inPath', action='store_true', dest='input_file', help='TrainingSet list file path',
                            default=config.CORPUS_PROCRSS_INPUT_FILE)
    dam_parser.add_argument('--debug', dest='d_cpName', help='Singleton Demo for test [CompName] build a result')
    dam_parser.add_argument('--sqlParams',  help='URL of heart beats', default=['limit:100', 'tabNum:2', 'random:Y'])
    dam_parser.set_defaults(mode='build_seg')

    seg_tr_parser = subparsers.add_parser('train_seg', help='Generate a classification training model')
    seg_tr_parser.add_argument('--phelp', action='store_true',  help='TrainingSet list file path')
    seg_tr_parser.add_argument('--crfparams', dest='options', help='General parameters provided by CRFs training', default='-f 1 -c 1')
    seg_tr_parser.add_argument('--templatePath', dest='template_file_path', help='The path to the feature template',
                               default=config.CLASSSIFY_TEMPLATE_FILE)
    seg_tr_parser.add_argument('--inPath', dest='corpus_file_path', help='Training model corpus path',
                               default=config.CLASSSIFY_TRAIN_CORPUS_FILE)
    seg_tr_parser.add_argument('--outFile', dest='out_path', help='Classification model generation path',
                               default=config.CLASSSIFY_MODEL_PATH+config.TIMESTAMP+'_crf_abbr_keep_model')
    seg_tr_parser.set_defaults(mode='train_seg')

    global G
    G = parser.parse_args()
    if str(G) == 'Namespace()':
        run()
    if G.mode == 'build_seg':
        pt = Pretreatment()
        if G.d_cpName:
            pt.one_parse(G.d_cpName)
        else:
            args = {'type': G.in_Type, 'mysqlParams': G.sqlParams, 'inputFile': G.input_file}
            print(''.join(['system out train params ', args]))
            pt.get_train_pretreatment(args)
    elif G.mode == 'load_seg':
        if G.detach:
            # running in background
            print(G.seg_pid)
            detach_proc(run, G.seg_pid)
        else:
            run()
    elif G.mode == 'train_seg':
        params = str(G.options).split(' ')
        if G.phelp:
            train_model(['-h'])
        else:
            train_model(params, template_file_path=G.template_file_path,
                        corpus_file_path=G.corpus_file_path,
                        out_path=G.out_path)

