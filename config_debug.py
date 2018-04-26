# -*- coding: UTF-8 -*-
import os


DEBUG = False

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
CORPUS_PROCRSS_RESULT_PATH = '/mnt/vol_0/wnd/usr/cmb_in/语料预处理结果/180425/'

#CRF模型路径
CRF_MODEL_FILE = '/mnt/vol_0/wnd/usr/cmb_in/模型文件/crf_model_180426.'