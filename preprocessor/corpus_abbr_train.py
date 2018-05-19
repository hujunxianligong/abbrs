# -*- coding: UTF-8 -*-
import os
import time

import config
import xlrd

from bin.term_tuple import AbbrChar
from load.load_reg_model import set_full_name, demo_convert_pinyinlist


def set_need_json(comapany, abbr, classifly_=None):
    # 获取第一阶段结果
    if not classifly_:
        term_list = set_full_name(comapany)
    else:
        term_list = set_full_name_2(comapany, classifly_)

    abbrs = []
    mark = 0
    for word in abbr:
        abbrs.append({"word": str(word)})
        for i in range(mark, len(term_list)):
            companyname_word = term_list[i].word
            if word == companyname_word:
                term_list[i].set_keep('K')
                mark = i + 1
                break

    full_name = []
    for term in term_list:
        try:
            full_name.append(term.set_json())
        except AttributeError as ex:
            print(ex)
    one_result = {"full_name": full_name, "abbrs": abbrs, "name": comapany}
    return one_result


def set_full_name_2(companyname,classifly_):

    pinyinlist = demo_convert_pinyinlist(companyname)
    termslist = []
    types = classifly_.split(' ')
    for one in types:
        word = one.split('_')[0]
        type_ = one.split('_')[1]
        i = 0
        for char in word:
            termslist.append(AbbrChar(char, type_ + str(i)))
            i += 1
    j = 0
    try:
        for pinyin in pinyinlist:
            tone = pinyin.getTone()
            termslist[j].set_tone(tone)
            j += 1
    except IndexError as ex:
        print(ex)
    return termslist


def get_trains_json(corpus_seg=None, timestamp=None):

    xlsx_file_path = config.ABBR_CORPUS_XLS_FILE
    if not timestamp:
        timestamp = str(int(time.time()))
    test_corpus_txt_path = config.ABBR_PRE_RE_PATH
    train_corpus_txt_file = ''.join([test_corpus_txt_path, timestamp, '_new_train_feature.crfpp'])

    std_sheet = xlrd.open_workbook(xlsx_file_path).sheet_by_index(0)
    output = open(train_corpus_txt_file, 'w+')
    if corpus_seg:
        test_coarse_grain_file = open(''.join([test_corpus_txt_path, '/', timestamp, '_coarse_grain_test']), 'w')
        test_fine_grain_file = open(''.join([test_corpus_txt_path, '/', timestamp, '_fine_grain_test']), 'w')

    for i in range(0, std_sheet.nrows):
        companyname = str(std_sheet.cell(i, 0).value).strip()
        classifly_ = str(std_sheet.cell(i, 1).value).strip()
        replace_chars = ['Ａ', '（', '）', '(', ')', '\n', ' ']
        for char in replace_chars:
            companyname = companyname.replace(char, '')
        for j in range(12):
            sheet_one = std_sheet.cell(i, j).value
            if sheet_one == 1 or sheet_one == 2:
                abbr = str(std_sheet.cell(i, j-1).value).replace(' ', '').strip()
                break
        blag = True
        igitnore_chars = ['ST', 'A', 'B', 'S', 'Ｂ']
        for char in igitnore_chars:
            if abbr.__contains__(char):
                blag = False
        for char in replace_chars:
            abbr = abbr.replace(char, '')
        if blag:
            if i % 500 == 0:
                print(i)
            # print(companyName, abbr)
            # trans_train_json = set_need_json(companyname, abbr)
            trans_train_json = set_need_json(companyname, abbr, classifly_)
            term_list = trans_train_json['full_name']
            sb = ''
            for term in term_list:
                sb = ''.join([sb, term['word'] + '\t' + str(term['tone'])
                              + '\t' + term['type_offset'] + '\t' + term['keep'] + '\n'])
                # sb = ''.join([sb, term['word'] + '\t' + term['type_offset'] + '\t' + term['keep'] + '\n'])
            if int(time.time()) % 10 % 5 == 3 and corpus_seg:
                test_coarse_grain_file.write(''.join([companyname, '\t', abbr, '\n']))
                test_fine_grain_file.write(sb+'\n')
            else:
                output.write(sb+'\n')
    output.close()
    if corpus_seg:
        test_coarse_grain_file.close()
        test_fine_grain_file.close()
        os.system("awk '{print $1}' "+test_coarse_grain_file.name+" > "+test_corpus_txt_path+'/'+timestamp+"_test_name")


if __name__ == '__main__':
    get_trains_json(True)
