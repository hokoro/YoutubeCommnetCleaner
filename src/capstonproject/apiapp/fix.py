from konlpy.tag import Okt
from hanspell import spell_checker


class Preprocessing:
    def __init__(self, Apath, Bpath):
        self.okt = Okt()
        self.bad_word_A_list = []
        self.bad_word_B_dict = {}
        with open(Apath, 'rt', encoding='UTF8') as file:
            for word in file.readlines():
                word = word.replace('\n', '')
                self.bad_word_A_list.append(word)
        with open(Bpath, 'rt', encoding='UTF8') as file:
            for word in file.readlines():
                divide = word.find(':')
                key = word[:divide]
                value = word[divide + 1:]
                self.bad_word_B_dict[key] = value

    def Spacing(self, comment):
        tagged = self.okt.pos(comment)
        fix_sentence = ''

        for word in tagged:
            if word[1] in ('Josa', 'PreEomi', 'Eomi', 'Suffix',
                           'Punctuation'):  # word[1] 품사의 종류 가 조사, 어미 ,접사 , 구두점 ,선어말 어미 띄어쓰기를 하지 않는 품사
                fix_sentence += word[0]
            else:
                fix_sentence += " " + word[0]  # 그외에는 띄어쓰기를 해야함
        if fix_sentence[0] == " ":  # 첫글자까 띄어쓰기 형태로 나올경우 를 대비
            fix_sentence = fix_sentence[1:]

        return fix_sentence

    def Bad_Word_Convert(self, comment):
        comment_list = comment.split(' ')
        fix_sentence = ''

        for i in range(len(comment_list)):
            if comment_list[i] in self.bad_word_A_list:
                fix_sentence = '대처 된 표현입니다'
                return fix_sentence
            elif comment_list[i] in self.bad_word_B_dict:
                comment_list[i] = self.bad_word_B_dict[comment_list[i]]
            else:
                continue

        text = ' '.join(comment_list)
        text = text.replace('\n', '')
        return text

    def Spell_Checker(self, comment):
        fix_sentence = spell_checker.check(comment)
        return fix_sentence.as_dict()['checked']
