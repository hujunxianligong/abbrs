# -*- coding: UTF-8 -*
import os

import CRFPP
import sys

import config

from bin.term_tuple import crf_reg_result, NameTerm, WordTerm

'''
成分识别类
包括加载crf模型 识别解析
'''
class RecCom:


    def __init__(self,modelFile):
        self.tagger = CRFPP.Tagger("-m " + modelFile)
        self.tagger.clear()
        self.begin = "#SENT_BEG#\tbegin"
        self.end = "#SENT_BEG#\tend"
        self.terms = []

    def _add(self,atts):
        result = '\t'.join(atts)
        self.tagger.add(result)

    def _addTerms(self,termList):
        self._add(self.begin)
        for term in termList:
            self._add(term)
        self._add(self.end)

    def _clear(self):
        self.terms.clear()
        self.tagger.clear()

    def _parse(self):
        if self.tagger.parse() == False:
            return self.terms
        for i in range(0,self.tagger.size()):
            test = self.tagger.y2(i)
            term = crf_reg_result(self.tagger.x(i, 0))
            term.set_wheater(self.tagger.y2(i))
            self.terms.append(term)
        return  self.terms

def reg_result_classify(company_name,richTermList):
    result = NameTerm(company_name)
    s_offset = 0
    e_offset = 0
    str = ''
    type = 'OUT'
    for richterm in richTermList:
        if richterm.char == '#':
            continue
        mark = richterm.wheater
        if 'R' in mark:
            type = 'R'
        elif 'I' in mark:
            type = 'I'
        elif 'U' in mark:
            type = 'U'
        elif 'O' in mark:
            type = 'O'

        if '_S' in mark:
            one = WordTerm(richterm.char, s_offset, e_offset)
            one.set_type(type)
            result.add_word_term(one)
            s_offset += 1
            e_offset += 1
        elif '_B' in mark:
            str = ''
            str = ''.join([str, richterm.char])
            e_offset += 1
        elif '_M' in mark:
            str = ''.join([str, richterm.char])
            e_offset += 1
        elif '_E' in mark:
            str = ''.join([str, richterm.char])
            one = WordTerm(str, s_offset, e_offset)
            one.set_type(type)
            result.add_word_term(one)
            str = ''
            e_offset += 1
            s_offset = e_offset
    if str.strip():
        one = WordTerm(str, s_offset, e_offset)
        one.set_type(type)
        result.add_word_term(one)
    return result

def get_model_abbr(company_name):
    fullname = list(company_name)
    recCom_instance = RecCom(config.CRF_MODEL_FILE)
    recCom_instance._addTerms(fullname)
    richTermList = recCom_instance._parse()
    result = reg_result_classify(company_name,richTermList)
    result.merge_wterm_include_type()
    print(result.set_api_json())
    recCom_instance._clear()

    return result

if __name__ == '__main__':
    get_model_abbr('三穗县顺景花场')