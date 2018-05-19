import os
import tempfile
import config
from jpype import *

from bin.jvm_crf_dic import HanlpJvm, crf_test
from bin.term_tuple import AbbrChar, AbbrWord
from load.load_model import get_model_abbr, RecCom
from util.tool import NLPDriver, test_asd, get_closest_file


def demo_convert_pinyinlist(name):
    if not isJVMStarted():
        HanlpJvm()

    tokenizer = JClass('com.hankcs.hanlp.HanLP')
    pinyinlist = tokenizer.convertToPinyinList(name)
    return pinyinlist


def set_full_name(name):
    cp_name = name
    replace_chars = ['（', '）', '(', ')', '\n', ' ']
    for char in replace_chars:
        cp_name = cp_name.replace(char, '')
    terms_list = []
    pinyinlist = demo_convert_pinyinlist(cp_name)
    if config.CLASSSIFY_MODEL_FILE:
        name_term = get_model_abbr(cp_name)
        for word_term in name_term.words_term:
            i = 0
            for char in word_term.word:
                terms_list.append(AbbrChar(char, word_term.type + str(i)))
                i += 1
    else:
        with NLPDriver('http://h133:5007/api/abbner', 5000) as driver:
            seg = driver.segment(cp_name.encode('UTF-8'))
            for term in seg:
                i = 0
                for word in term['word']:
                    terms_list.append(AbbrChar(word, term['type'] + str(i)))
                    i += 1
    j = 0
    try:
        for pinyin in pinyinlist:
            tone = pinyin.getTone()
            terms_list[j].set_tone(tone)
            j += 1
    except IndexError as ex:
        print(ex)
    return terms_list


def tran_test_corpus(arg):
    if not arg:
        return None
    test_file = tempfile.NamedTemporaryFile()
    sb = ''
    if isinstance(arg, list):
        for cp_name in arg:
            termlist = set_full_name(cp_name)
            for term in termlist:
                sb = ''.join([sb, str(term), '\n'])
            sb = ''.join([sb, '\n'])
    elif isinstance(arg, str):
        termlist = set_full_name(arg)
        for term in termlist:
            sb = ''.join([sb, str(term), '\n'])
        sb = ''.join([sb, '\n'])

    test_file.write(sb.encode('utf-8'))
    return test_file


def write_back_result(readlines,outputfile):
    abb_results = {}
    abbr_list = []
    for line in readlines:
        if line == b'\n':
            one_abb_result = AbbrWord(abbr_list)
            full_name = one_abb_result.full_name
            if full_name in abb_results:
                abbrs = abb_results.get(full_name)
                abbr = one_abb_result.get_abb()
                if abbr.strip() and abbr not in abbrs:
                    abbrs.append(abbr)
                    #abb_results.update({full_name: abbrs})
            else:
                abb_results[full_name] = [one_abb_result.get_abb()]
            abbr_list.clear()
        elif line.decode('UTF-8').startswith("#"):
            continue
        else:
            strs = line.decode('UTF-8').replace('\n', '').split('\t')
            one_abbr_word = AbbrChar(strs[0], strs[2])
            one_abbr_word.set_tone(strs[1])
            one_abbr_word.set_wheater(strs[3])
            abbr_list.append(one_abbr_word)

    for (k, v) in abb_results.items():
        ltc_abb_list = load_ltd_cp_abbr(k)
        if len(v) < 2:
            for abbr in ltc_abb_list:
                if abbr not in v:
                    v.append(abbr)
        else:
            redup_ltc_abb_list = []
            for abbr in ltc_abb_list:
                if abbr not in v:
                    redup_ltc_abb_list.append(abbr)
            v[2:2] = redup_ltc_abb_list

    with open(outputfile, 'w') as f:
        for (k, v) in abb_results.items():
            lists = [k+'\t'+line + '\n' for line in v]
            # lists = [k+'\t'+str(v) + '\n' ]
            f.writelines(lists)
    f.close()

    return abb_results


def load_ltd_cp_abbr(company_name):
    fullname = set_full_name(company_name)
    rm_instance = RecCom('/home/hadoop/wnd/usr/crf_cp_name_easy/171213_first_model/new_abbr_feature.crfpp', 2)
    rm_instance.addterms(fullname)
    rich_termlist = rm_instance.parse()
    abbrlist = []
    for termlist in rich_termlist:
        sb = ''
        for term in termlist:
            if term.wheater == 'K':
                sb = ''.join([sb, term.char])
            if sb.strip() and sb not in abbrlist and len(sb) > 1:
                abbrlist.append(sb)
    return abbrlist


def load_model(arg, model_file_path=None, output_file_path=None):
    if isinstance(arg, list):
        params = arg[:len(arg) - 1]
        arg = arg[-1]
    else:
        params = None

    if os.path.exists(arg):
        with open(arg, 'r') as fp:
            lines = fp.readlines()
            test_file = tran_test_corpus(lines)
    else:
        test_file = tran_test_corpus(arg)
        test_file.seek(0)
    if not model_file_path:
        model_file_path = config.ABBR_MODEL_FILE
        if not os.path.exists(model_file_path):
            model_file_path = get_closest_file(config.ABBR_TRAIN_MODEL_PATH, '_crf_abbr_keep_model')
    if not output_file_path:
        tmp_outfile = tempfile.mkstemp()
        output_file_path = tmp_outfile[1]
        print('输出路径为%s', output_file_path)

    tmp_file = tempfile.NamedTemporaryFile()
    try:
        general_params = ['-m', model_file_path, test_file.name, '-o', tmp_file.name]
    except AttributeError as ex:
        print(ex)
    if not params:
        new_args = general_params
    else:
        params.extend(general_params)
        new_args = params

    crf_test(new_args)

    lines = tmp_file.readlines()
    abbrs_results = write_back_result(lines, output_file_path)
    return output_file_path, abbrs_results

if __name__ == '__main__':
    options = ['-n', '2', '-v', '0', '华为技术有限公司']
    demo_convert_pinyinlist('华为技术有限公司')
    #learn_model(options)
    # load_model(['-n', '5', '-v', '0', '/mnt/vol_0/wnd/usr/cmb_in/ing简称名单/180518/error_name.txt'], \
    #             model_file_path='/mnt/vol_0/wnd/usr/cmb_in/模型文件/1526474342_crf_abbr_keep_model')
    #print(load_ltd_cp_abbr('华为技术有限公司'))
    while True:
        load_model('华为技术有限公司')
   # crf_test.crf_learn(['-h'])
