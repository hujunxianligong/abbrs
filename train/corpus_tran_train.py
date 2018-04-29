# -*- coding: UTF-8 -*-
import re
import time

from pyhanlp import HanLP

import config
from bin.term_tuple import NameTerm, WordTerm, CharTerm, WORD_TYPE
from train.get_corpus import get_sql_cpname

from util.tool import read_dic

class Pretreatment:
    def __init__(self):
        # 加载词典
        self.region_dic = read_dic(config.PLACE_FILE)
        self.industry_dic = read_dic(config.INDUSTRY_FILE)
        self.organization_dic = read_dic(config.ORGANIZATION_FILE)


    def get_train_pretreatment(self,type,inputfile):
        """
        @summary:根据公司名单得到规整训练集，用于训练
         @params：type 控制数据源来源，主要是文本跟数据库参数 mysql/None ,inputfile 文件路径，使用数据库链接时可以为None
         @return:配置文件中已经设置了输出路径 ，这里无返回
        """

        #获取语料
        if type == 'mysql' and config.MYSQL_ENABLE:
            unprocessed_corpus = get_sql_cpname(['limit:10','tabNum:2','random:Y'])
        else:
            unprocessed_corpus = read_dic(inputfile)
        #加工语料
        cp_term_list = []
        for companyname in unprocessed_corpus:
            if isinstance(companyname,tuple):
                cp_name = companyname[0].strip()
                cp_term = self.one_parse(cp_name)
                cp_term_list.append(cp_term)
            elif isinstance(companyname,str):
                cp_name = companyname
                cp_term = self.one_parse(cp_name)
                cp_term_list.append(cp_term)
        #写出返回
        t = ''.join([str(int(time.time())),'_'])
        companyname_outPath = ''.join([config.CORPUS_PROCRSS_RESULT_PATH,t,'companyname'])
        crfpp_outPath = ''.join([config.CORPUS_PROCRSS_RESULT_PATH,t,'set_crf++_model'])
        json_outPath = ''.join([config.CORPUS_PROCRSS_RESULT_PATH,t,'corpus_Visual.json'])
        cpout = open(companyname_outPath, 'w+')
        outPut = open(crfpp_outPath, 'w+')
        jsonout = open(json_outPath, 'w+')
        for cp in cp_term_list:
            cpout.write(''.join([cp.company_name,'\n']))
            sb = '#SENT_BEG#\tbegin\n'
            sb = ''.join([sb,cp.name_crf_model()])
            sb = ''.join([sb, '#SENT_END#\tend\n\n'])
            outPut.write(str(sb))
            jsonout.write(''.join([cp.name_to_json(),'\n']))
        jsonout.close()
        outPut.close()
        cpout.close()
        return



    def one_parse(self,cp):
        print(cp)
        cp = re.sub('[\(（）\)]', '', cp)
        cp_term = NameTerm(cp)
         # 获取单词与词性
        segments=HanLP.segment(cp)
        print(str(segments))
        self.match_word_type(cp_term, 'region', self.region_dic)
        self.match_word_type(cp_term, 'organization', self.organization_dic)
        self.match_word_type(cp_term, 'industry', self.industry_dic)
        #self.match_seg_word_type(cp_term, segments, 'region', self.region_dic)
        self.match_seg_word_type(cp_term, segments, 'organization', self.organization_dic)
        self.match_seg_word_type(cp_term, segments, 'industry', self.industry_dic)
        self.get_unknown_type(cp_term)
        cp_term.sort_word_term()
        cp_term.deduplication_word()
        print(cp_term.set_api_json())
        return cp_term

    def match_seg_word_type(self,cp_term,seg_ments,type_name,type_dic):
        c_index = 0
        for segment in seg_ments:

            if segment.word in type_dic:
                self.struct_word_terms(cp_term, segment.word, c_index, type_name)
            c_index += len(segment.word)

    def match_word_type(self,cp_term,type_name,type_dic):
        cp_name =cp_term.company_name
        for type_word in type_dic:
            c_index = 0
            if type_word in cp_name:
                while True:
                    c_index = cp_name.find(type_word, c_index)
                    if c_index > -1 and c_index <= len(cp_name) - 1:
                        if cp_term.iswordUse(c_index,type_word):
                            self.struct_word_terms(cp_term, type_word, c_index, type_name)
                            c_index += len(type_word)
                        else:
                            break
                    else:
                        break

    def get_unknown_type(self,cp_term):
        cp_name = cp_term.company_name
        for word_term in cp_term.words_term:
            replace_word = ''
            for i in word_term.word:
                replace_word = ''.join([replace_word,'$'])
            cp_name = cp_name[:word_term.s_offset]+replace_word+cp_name[word_term.e_offset+1:]
        split_list = cp_name.split('$')
        index = 0
        for unknown in  split_list:
            unword = unknown.strip()
            if unword:
                index = cp_name.find(unword, index)
                self.struct_word_terms(cp_term, unword, index, 'unkown')


    def struct_word_terms(self,cp_term,word,index,type_name):
        cp_name = cp_term.company_name
        word_term = WordTerm(word, index, index + len(word) - 1)
        word_term.set_type(WORD_TYPE[type_name])
        se_index = index
        for s_char in word:
            se_index = cp_name.find(s_char, se_index)
            char_term = CharTerm(s_char, se_index, type_name)
            char_term.char_position(index, index + len(word) - 1, se_index)
            word_term.add_char_term(char_term)
        cp_term.add_word_term(word_term)


if __name__ == '__main__':
    pt = Pretreatment()
    pt.get_train_pretreatment('mysql',"/mnt/vol_0/wnd/usr/cmb_in/语料预处理结果/180427/1524934560_companyname")
    #pt.one_parse('山东海力化工股份有限公司')