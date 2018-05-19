# -*- coding: UTF-8 -*-
import os
import pathlib

import time

DEBUG = False

basedir = os.path.abspath(os.path.dirname(__file__))
DEFAULT_LOGDIR = os.path.join(basedir, '..', 'log')
TODAY_DIR = time.strftime('%y%m%d', time.localtime(time.time()))
TIMESTAMP = str(int(time.time()))

SEG_API_PID_FILE = 'seg_api.pid'
SEG_API_PORT = 5007

ROOT_DIR = '/mnt/vol_0/wnd/usr/cmb_in'

if not os.path.exists(ROOT_DIR):
    ROOT_DIR = os.path.join(basedir, '..', 'cmb_abbr')

# 日志配置
LOG_DIR = DEFAULT_LOGDIR
LOG_FORMAT = '%(asctime)s %(process)d %(levelname)s: %(message)s [in %(module)s.%(funcName)s:%(lineno)d]'
LOG_LEVEL = 'debug'
MAX_BYTES = 100 * 1024 * 1024  # 100M
BACKUP_COUNT = 5

# 数据库配置
MYSQL_HOST = "h131"
MYSQL_PORT = 13306
MYSQL_USER = "wnd"
MYSQL_PASS = "wangniasd1"
MYSQL_DB = "tree_development"

'''
简称第一阶段分类参数
'''
CLASSIFY_DIR = os.path.join(ROOT_DIR, 'classify_stage')
# 词典路径
PLACE_FILE = CLASSIFY_DIR + '/dic/地名.txt'
INDUSTRY_FILE = CLASSIFY_DIR + '/dic/行业名称.txt'
ORGANIZATION_FILE = CLASSIFY_DIR + '/dic/组织形式.txt'

# 语料处理输入文件
CORPUS_PROCRSS_INPUT_FILE = CLASSIFY_DIR+'/corpus/'+'1525001802_companyname'
# 语料处理结果路径
CORPUS_PROCRSS_RESULT_PATH = CLASSIFY_DIR+'/pretreatment/'+TODAY_DIR + '/'
if not os.path.exists(CORPUS_PROCRSS_RESULT_PATH):
    os.makedirs(CORPUS_PROCRSS_RESULT_PATH)
# 分类训练集路径
CLASSSIFY_TRAIN_CORPUS_FILE = CORPUS_PROCRSS_RESULT_PATH+'1526707603_set_crf++_model'
# 名称分类 特征模板
CLASSSIFY_TEMPLATE_FILE = CLASSIFY_DIR+'/template/template0'
# 简称缩略训练结果模型存放地址
CLASSSIFY_MODEL_PATH = CLASSIFY_DIR+'/model/'
# CRF模型路径
CLASSSIFY_MODEL_FILE = CLASSSIFY_MODEL_PATH + '1526707640_crf_abbr_classify_model'


'''
简称第二阶段生成参数
'''
GENERATE_DIR = os.path.join(ROOT_DIR, 'generate_stage')
# 第二阶段语料表
ABBR_CORPUS_XLS_FILE = GENERATE_DIR+'/corpus/'+'5000简称标注.xls'
# 语料处理结果保持目录，包含训练集和测试集文件存放处
ABBR_PRE_RE_PATH = GENERATE_DIR+'/pretreatment/'+TODAY_DIR + '/'
if not os.path.exists(ABBR_PRE_RE_PATH):
    os.makedirs(ABBR_PRE_RE_PATH)
# 第三方JAVA依赖报路径
THIRD_JAVA_CLASS_PATH = GENERATE_DIR+'/jar/'
# 第三方分词工具hanlp
HANLP_PROPERTIES_FILE_PATH = THIRD_JAVA_CLASS_PATH+'/hanlp.properties'
# 自制CRF构造器名称
# CRF_CONST_JAR_PATH = 'crf4j-0.58-SNAPSHOT-jar-with-dependencies.jar'
# 简称生成CRF 特征模板
ABBR_FEATURE_TEMPLATE = GENERATE_DIR+'/template/template'
# 简称缩略训练集语料路径 ,分类后第二部操作
ABBR_TRAIN_CORPUS_FILE = ABBR_PRE_RE_PATH+'1526419651_new_train_feature.crfpp'
# 简称缩略训练结果模型存放地址
ABBR_TRAIN_MODEL_PATH = GENERATE_DIR+'/model/'
# 简称缩略模型加载路径
ABBR_MODEL_FILE = ABBR_TRAIN_MODEL_PATH+'1526710438_crf_abbr_keep_model'


MYSQL_ENABLE = True
if DEBUG:
    import config_debug

    ROOT_DIR = config_debug.ROOT_DIR
