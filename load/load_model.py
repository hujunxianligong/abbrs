# -*- coding: UTF-8 -*
from jpype import JClass

import config
from bin.jvm_crf_dic import SPCrf
from logger_manager import seg_api_logger as logger
from bin.term_tuple import CrfRegResult, NameTerm, WordTerm


class RecCom:
    def __init__(self, modelfile=None, nbest=None,):

        if not nbest:
            nbest = 1
        if not modelfile:
            assert False

        ModelImpl = JClass('com.github.zhifac.crf4j.ModelImpl')
        self.model = ModelImpl()
        self.model.open(modelfile, nbest, 0, 1.0)

        self.tagger = self.model.createTagger()
        # self.tagger = CRFPP.Tagger('-n '+str(nbest)+' -m ' + modelfile)

        self.tagger.clear()
        self.begin = "#SENT_BEG#\tbegin"
        self.end = "#SENT_BEG#\tend"
        self.terms = []

    def _add(self, atts):
        result = '\t'.join(str(atts))
        self.tagger.add(result)

    def addterms(self, termlist):
        self._add(self.begin)
        for term in termlist:
            self._add(term)
        self._add(self.end)

    def clear(self):
        self.terms.clear()
        self.tagger.clear()

    def parse(self):
        if not self.tagger.parse():
            return self.terms
        # for i in range(0, self.tagger.size()):
        #     term = crf_reg_result(self.tagger.x(i, 0))
        #     term.set_wheater(self.tagger.y2(i))
        #     self.terms.append(term)

        #for n in range(self.tagger.nbest()):
        for n in range(self.model.getNbest_()):
            if not self.model.getNbest_():
                break
            termlist = []
            for i in range(self.tagger.size()):
                term = CrfRegResult(self.tagger.x(i, 0))
                term.set_wheater(self.tagger.yname(self.tagger.y(i)))
                termlist.append(term)
            self.terms.append(termlist)
        return self.terms


def reg_result_classify(company_name, rich_termlist):
    result = NameTerm(company_name)
    s_offset = 0
    e_offset = 0
    word_str = ''
    word_type = 'OUT'
    for richterm in rich_termlist:
        if richterm.char == '#':
            continue
        before_type = word_type
        mark = richterm.wheater
        if 'R' in mark:
            word_type = 'R'
        elif 'I' in mark:
            word_type = 'I'
        elif 'U' in mark:
            word_type = 'U'
        elif 'O' in mark:
            word_type = 'O'

        if '_S' in mark:
            if word_str.strip():
                one = WordTerm(word_str, s_offset, e_offset-1)
                one.set_type(before_type)
                result.add_word_term(one)
                s_offset = e_offset
            one = WordTerm(richterm.char, s_offset, e_offset)
            one.set_type(word_type)
            result.add_word_term(one)
            s_offset += 1
            e_offset += 1
            word_str = ''
        elif '_B' in mark:
            if word_str.strip():
                one = WordTerm(word_str, s_offset, e_offset-1)
                one.set_type(before_type)
                result.add_word_term(one)
                s_offset = e_offset
            word_str = ''
            word_str = ''.join([word_str, richterm.char])
            e_offset += 1
        elif '_M' in mark:
            word_str = ''.join([word_str, richterm.char])
            e_offset += 1
        elif '_E' in mark:
            word_str = ''.join([word_str, richterm.char])
            one = WordTerm(word_str, s_offset, e_offset)
            one.set_type(word_type)
            result.add_word_term(one)
            word_str = ''
            e_offset += 1
            s_offset = e_offset
    if word_str.strip():
        one = WordTerm(word_str, s_offset, e_offset)
        one.set_type(word_type)
        result.add_word_term(one)
    return result


def get_model_abbr(company_name, g=None):
    fullname = list(company_name)
    SPCrf()

    if g and not str(g) == 'Namespace()':
        rm_instance = RecCom(g.load_model_path)
    else:
        rm_instance = RecCom(config.CLASSSIFY_MODEL_FILE)
        rm_instance.addterms(fullname)
    rich_termlist = rm_instance.parse()
    result = reg_result_classify(company_name, rich_termlist[0])
    result.merge_wterm_include_type(None)
    logger.info(result.set_api_json())
    rm_instance.clear()
    return result


if __name__ == '__main__':
    print(get_model_abbr('中国电建集团成都勘测设计研究院有限公司').set_api_json())
