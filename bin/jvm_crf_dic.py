# -*- coding: UTF-8 -*
import os

import config
from jpype import *
from logger_manager import reg_api_logger as logger


class HanlpJvm:
    def __init__(self):
        if not isJVMStarted():
            self.startup_jvm()

    @staticmethod
    def startup_jvm():
        java_class_path = ''
        for file in os.listdir(config.THIRD_JAVA_CLASS_PATH):
            if file.endswith('jar'):
                java_class_path +=config.THIRD_JAVA_CLASS_PATH+file+":"
        #java_class_path = config.THIRD_JAVA_CLASS_PATH + '/'+config.CRF_CONST_JAR_PATH + ':'+config.HANLP_JAR_PATH
        try:
            startJVM(getDefaultJVMPath(), '-Djava.class.path=' + java_class_path, '-Xms1g', '-Xmx1g')
        except JavaException as ex:
            if ex is java.lang.RuntimeException:
                logger.error("Caught the runtime exception : ", JavaException.message())
                logger.error(JavaException.stackTrace())
        predefine = JClass('com.hankcs.hanlp.utility.Predefine')
        predefine.HANLP_PROPERTIES_PATH = config.HANLP_PROPERTIES_FILE_PATH

    @staticmethod
    def shut_jvm():
        shutdownJVM()


def crf_learn(args):
    # c_crf_learn = JClass('com.github.zhifac.crf4j.CrfLearn')
    cmd_str = 'crf_learn'
    for param in args:
        cmd_str += ''.join([' ', param])
    logger.info(cmd_str)
    os.system(cmd_str)


def crf_test(args):
    # c_ctf_test = JClass('com.github.zhifac.crf4j.CrfTest')
    cmd_str = 'crf_test'
    for param in args:
        cmd_str += ''.join([' ', param])
    logger.info(cmd_str)
    os.system(cmd_str)

