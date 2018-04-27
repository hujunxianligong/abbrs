# -*- coding: UTF-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

# 词典路径
PLACE_FILE = "/home/hadoop/wnd/usr/crf_cp_name_easy/abb/resources/地名.txt"
INDUSTRY_FILE = "/home/hadoop/wnd/usr/crf_cp_name_easy/abb/resources/行业名称.txt"
ORGANIZATION_FILE = "/home/hadoop/wnd/usr/crf_cp_name_easy/abb/resources/组织形式.txt"

# 数据库配置
MYSQL_HOST = "h131"
MYSQL_PORT = 13306
MYSQL_USER = "wnd"
MYSQL_PASS = "wangniasd1"
MYSQL_DB = "tree_development"

# 语料处理结果路径
CORPUS_PROCRSS_RESULT_PATH = '/mnt/vol_0/wnd/usr/cmb_in/语料预处理结果/180427/'

#CRF模型路径
CRF_MODEL_FILE = '/home/hadoop/abbreviation/abbs_seg/model/crf_model_180426.'



if DEBUG:
    import config_debug

    PLACE_FILE = config_debug.PLACE_FILE
    INDUSTRY_FILE = config_debug.INDUSTRY_FILE
    ORGANIZATION_FILE = config_debug.ORGANIZATION_FILE

    MYSQL_HOST = config_debug.MYSQL_HOST
    MYSQL_PORT = config_debug.MYSQL_PORT
    MYSQL_USER = config_debug.MYSQL_USER
    MYSQL_PASS = config_debug.MYSQL_PASS
    MYSQL_DB = config_debug.MYSQL_DB

    CORPUS_PROCRSS_RESULT_PATH = config_debug.CORPUS_PROCRSS_RESULT_PATH
    CRF_MODEL_FILE =config_debug.CRF_MODEL_FILE