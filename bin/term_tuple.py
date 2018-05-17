# coding=UTF-8


class AbbrWord:
    def __init__(self, abb_chars):
        self.abb = ''
        self.full_name = ''
        for abb_char in abb_chars:
            if abb_char.wheater == 'K':
                self.abb = ''.join([self.abb, abb_char.word])
            self.full_name = ''.join([self.full_name, abb_char.word])

    def get_abb(self):
        return self.abb

    def show(self):
        return ''.join([self.full_name, '\t', self.abb])


class AbbrChar:

    def __init__(self, word, type_offset):
        self.word = word
        self.type_offset = type_offset
        self.wheater = 'S'
        self.tone = str(5)

    def set_wheater(self, wheater):
        self.wheater = wheater

    def set_tone(self, tone):
        self.tone = str(tone)

    def __str__(self):
        result = ''.join([self.word, '\t',  str(self.tone), '\t', str(self.type_offset)])
        # result = ''.join([self.word,  '\t', str(self.type_offset)])
        return str(result)

    def set_keep(self, keep):
        self.wheater = keep

    def set_json(self):
        result = {"word": str(self.word), "type_offset": str(self.type_offset),
                  "tone": self.tone, "keep": str(self.wheater)}
        # result = {"word": str(self.word), "type_offset": str(self.type_offset), "keep": str(self.wheater)}
        return result


class CrfRegResult:
    def __init__(self, char):
        self.char = char
        self.wheater = 'S'

    def set_wheater(self, wheater):
        self.wheater = wheater

    def __str__(self):
        result = {'char': self.word}
        return str(result)

    def set_result(self, result):
        self.wheater = result

    def set_json(self):
        result = {"char": str(self.word), "result": str(self.wheater)}
        return result


class NameTerm:
    def __init__(self, companyname):
        self.company_name = companyname
        self.words_term = []
        self.before_merge_words_term = []

    def remove_word_term(self, index):
        words_term = self.words_term
        for i, word_term in enumerate(words_term):
            if index == i:
                words_term.remove(word_term)
                return

    def merge_wterm_include_type(self, type):
        self.before_merge_words_term.clear()
        if len(self.words_term) <= 1:
            self.before_merge_words_term = self.words_term
            return

        for word_term in self.words_term:
            self.before_merge_words_term.append(word_term)

        self.words_term.clear()
        first_flag = True

        for word_term in self.before_merge_words_term:
            if first_flag:
                before = word_term
                first_flag = False
                continue
            if before.type == word_term.type:
                if not type or type in before.type :
                    before.e_offset += len(word_term.word)
                    before.word = ''.join([before.word,word_term.word])
                else:
                    self.add_word_term(before)
                    before = word_term
            else:
                if not before:
                    self.add_word_term(word_term)
                else:
                    self.add_word_term(before)
                    before = word_term
        self.add_word_term(before)

    def add_word_term(self, word_term):
        self.words_term.append(word_term)

    def is_word_use(self, index, word):
        if not self.words_term:
            return True
        for word_term in self.words_term:
            if (word_term.e_offset >= index >= word_term.s_offset) \
                    or (word_term.e_offset >= index + len(word) - 1 and word_term.s_offset <= index + len(word)-1):
                return False
        return True

    def sort_word_term(self):
        if len(self.words_term):
            self.words_term.sort(key=lambda WordTerm: (WordTerm.s_offset, -len(WordTerm.word)))

    def deduplication_word(self):
        if len(self.words_term) <= 1:
            return
        tmp_term = []
        for word_term in self.words_term:
            tmp_term.append(word_term)

        self.words_term.clear()
        first_flag = True
        for term in tmp_term:
            if first_flag:
                b_term = term
                first_flag = False
                continue
            if term.s_offset <= b_term.e_offset:
                continue
            else:
                self.add_word_term(b_term)
            b_term = term
        self.add_word_term(b_term)

    def name_crf_model(self):
        name_demo = ''
        for word in self.words_term:
            name_demo = ''.join([name_demo, word.word_crf_model()])
        return name_demo

    def set_api_json(self):
        import json
        api_json = []
        for word in self.words_term:
            api_json.append(json.loads(word.set_api_json()))
        json = json.dumps(api_json, sort_keys=True, ensure_ascii=False)
        return json

    def name_to_json(self):
        import json
        name_term_json = []
        for word in self.words_term:
            name_term_json.append(json.loads(word.word_to_json()))
        data = {'company_name': self.company_name, 'word_term': name_term_json}
        json = json.dumps(data, sort_keys=True, ensure_ascii=False)
        return json


class WordTerm:
    def __init__(self, word, start_offset, end_offset):
        self.word = word
        self.s_offset = start_offset
        self.e_offset = end_offset
        self.chars_term = []
        self.type = ''

    def set_type(self, word_type):
        self.type = word_type

    def add_char_term(self, char_term):
        self.chars_term.append(char_term)

    def word_crf_model(self):
        word_demo = ''
        for char in self.chars_term:
            word_demo = ''.join([word_demo, char.char_crf_model(), '\n'])
        return word_demo

    def set_api_json(self):
        import json
        data = {'word': self.word, 'type': self.type}
        json = json.dumps(data, sort_keys=True, ensure_ascii=False)
        return json

    def word_to_json(self):
        import json
        chars_term_json = []
        for char in self.chars_term:
            chars_term_json.append(json.loads(char.char_to_json()))
        data = {'word': self.word, 's_offset': self.s_offset, 'e_offset': self.e_offset, 'chars_term': chars_term_json}
        json = json.dumps(data, sort_keys=True,  ensure_ascii=False)
        return json


class CharTerm:
    def __init__(self, cp_char, offset, char_type):
        self.cp_char = cp_char
        self.offset = offset
        self.mark = WORD_TYPE[char_type]

    def char_position(self, s_offset, e_offset, offset):
        if s_offset == e_offset:
            self.mark = ''.join([self.mark, CHAR_LOCATE['single']])
        elif s_offset == offset:
            self.mark = ''.join([self.mark, CHAR_LOCATE['begin']])
        elif e_offset == offset:
            self.mark = ''.join([self.mark, CHAR_LOCATE['end']])
        else:
            self.mark = ''.join([self.mark, CHAR_LOCATE['middle']])

    def char_crf_model(self):
        return '%s\t%s' % (self.cp_char, self.mark)

    def char_to_json(self):
        import json
        data = {'char': self.cp_char, 'offset': self.offset, 'mark': self.mark}
        json = json.dumps(data, sort_keys=True, ensure_ascii=False)
        return json


WORD_TYPE = {
    'region': 'R',
    'industry': 'I',
    'unkown': 'U',
    'organization': 'O',
}

CHAR_LOCATE = {
    'single': '_S',
    'begin': '_B',
    'end': '_E',
    'middle': '_M',
}
