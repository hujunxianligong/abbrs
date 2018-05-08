# -*- coding: UTF-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))
DEFAULT_LOGDIR = os.path.join(basedir, '..', 'log')

DEBUG = True


SEG_API_PID_FILE = 'seg_api.pid'
SEG_API_PORT = 5007

# 词典路径
PLACE_FILE = "/home/hadoop/wnd/usr/crf_cp_name_easy/abb/resources/地名.txt"
INDUSTRY_FILE = "/home/hadoop/wnd/usr/crf_cp_name_easy/abb/resources/行业名称.txt"
ORGANIZATION_FILE = "/home/hadoop/wnd/usr/crf_cp_name_easy/abb/resources/组织形式.txt"
# 日志配置
LOG_DIR = DEFAULT_LOGDIR
LOG_FORMAT = '%(asctime)s %(process)d %(levelname)s: %(message)s [in %(module)s.%(funcName)s:%(lineno)d]'
LOG_LEVEL = 'debug'
MAX_BYTES = 100 * 1024 * 1024 # 100M
BACKUP_COUNT = 5

# 数据库配置
MYSQL_HOST = "h131"
MYSQL_PORT = 13306
MYSQL_USER = "wnd"
MYSQL_PASS = "wangniasd1"
MYSQL_DB = "tree_development"

# 语料处理输入路径
CORPUS_PROCRSS_INPUT_PATH = '/mnt/vol_0/wnd/usr/cmb_in/语料预处理结果/180504/1525001802_companyname'
# 语料处理结果路径
CORPUS_PROCRSS_RESULT_PATH = '/mnt/vol_0/wnd/usr/cmb_in/语料预处理结果/180504/'

#CRF模型路径
CRF_MODEL_FILE = '/home/hadoop/abbreviation/abbs_seg/model/crf_model_180426.'

MYSQL_ENABLE = True

if DEBUG:
    import config_debug

    PLACE_FILE = config_debug.PLACE_FILE
    INDUSTRY_FILE = config_debug.INDUSTRY_FILE
    ORGANIZATION_FILE = config_debug.ORGANIZATION_FILE

    CORPUS_PROCRSS_RESULT_PATH = config_debug.CORPUS_PROCRSS_RESULT_PATH
    CRF_MODEL_FILE =config_debug.CRF_MODEL_FILE