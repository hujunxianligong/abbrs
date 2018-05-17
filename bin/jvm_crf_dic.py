# -*- coding: UTF-8 -*
import os

import config
from jpype import *


class SPCrf:
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
            print(get_default_jvm_path())
            startJVM(getDefaultJVMPath(), '-Djava.class.path=' + java_class_path, '-Xms1g', '-Xmx1g')
        except JavaException as ex:
            if ex is java.lang.RuntimeException:
                print("Caught the runtime exception : ", JavaException.message())
                print(JavaException.stackTrace())
        predefine = JClass('com.hankcs.hanlp.utility.Predefine')
        predefine.HANLP_PROPERTIES_PATH = config.HANLP_PROPERTIES_FILE_PATH

    @staticmethod
    def shut_jvm():
        shutdownJVM()

    def crf_learn(self, args):
        if not isJVMStarted():
            self.startup_jvm()
        c_crf_learn = JClass('com.github.zhifac.crf4j.CrfLearn')
        assert c_crf_learn.run(args)

    def crf_test(self, args):
        if not isJVMStarted():
            self.startup_jvm()
        c_ctf_test = JClass('com.github.zhifac.crf4j.CrfTest')
        assert c_ctf_test.run(args)
if __name__ == '__main__':
    SPCrf()
