import tensorflow as tf
import numpy as np
import os
import fasttext
from jamo import h2j, j2hcj


# import pandas as pd


class model1_application:
    def __init__(self, Aipath, Fasttextpath):
        fasttext.FastText.eprint = lambda x: None
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        self.Ai_model = tf.keras.models.load_model(Aipath)  # LSTM Model Load  / Aipath 는 model 파일의 경로
        self.Fasttext_model = fasttext.load_model(Fasttextpath)  # Fasttext model Load /Fasttextpath 는 Model 의 파일 경로
        self.sentence_number = 25  # 문장 단어수 제한

    def model_test(self, comment_list):
        for comment_info in comment_list:
            test_word = j2hcj(
                h2j(comment_info['text'])) + ' '  # comment_info 의 댓글 정보 를 가져와서 초성/중성/종성 으로 분리 (ex) 바보  -> ㅂ ㅏ ㅂ ㅗ)
            test_word_split = test_word.split()  # 해당 단어를 스페이스 를 기준으로 split
            fast_vec = []  # fast 모델의 적용한 후 input vector 를 담아두는 리스트
            for index in range(self.sentence_number):  # 해당 글자수 까지 체크를 하여
                if index < len(test_word_split):  # 해당 단어수 보다 index 가 작으면
                    fast_vec.append(self.Fasttext_model[test_word_split[index]])  # 해당 단어를 fasttext model 에 적용
                else:
                    fast_vec.append(np.array([0] * 100))  # 단어 수가 넘어가면 input 크기를 맞추기 위해 padding 을 numpy 형식으로 적용

            fast_vec = np.array(fast_vec)  # 현재 리스트 형태로 저장된 데이터를 numpy 형식으로 재 변환
            fast_vec = fast_vec.reshape(1, fast_vec.shape[0], fast_vec.shape[1])  # 3차원으로 크기 조절 input type (1,25,100)

            test_pre = self.Ai_model.predict([fast_vec]).argmax()  # 해당 데이터를 인공지능 모델에 적용

            # 해당 comment_info 정보를 label 에 맞춰서 저장
            if test_pre == 0:
                comment_info['label'] = '긍정'
            elif test_pre == 1:
                comment_info['label'] = '부정'
            elif test_pre == 2:
                comment_info['label'] = '악플'

        return comment_list  # 해당 댓글을 리턴

    def Model_test_demo(self, comment_list):
        for comment_info in comment_list:
            test_word = j2hcj(
                h2j(comment_info['Comment'])) + ' '  # comment_info 의 댓글 정보 를 가져와서 초성/중성/종성 으로 분리 (ex) 바보  -> ㅂ ㅏ ㅂ ㅗ)
            test_word_split = test_word.split()  # 해당 단어를 스페이스 를 기준으로 split
            fast_vec = []  # fast 모델의 적용한 후 input vector 를 담아두는 리스트
            for index in range(self.sentence_number):  # 해당 글자수 까지 체크를 하여
                if index < len(test_word_split):  # 해당 단어수 보다 index 가 작으면
                    fast_vec.append(self.Fasttext_model[test_word_split[index]])  # 해당 단어를 fasttext model 에 적용
                else:
                    fast_vec.append(np.array([0] * 100))  # 단어 수가 넘어가면 input 크기를 맞추기 위해 padding 을 numpy 형식으로 적용

            fast_vec = np.array(fast_vec)  # 현재 리스트 형태로 저장된 데이터를 numpy 형식으로 재 변환
            fast_vec = fast_vec.reshape(1, fast_vec.shape[0], fast_vec.shape[1])  # 3차원으로 크기 조절 input type (1,25,100)

            test_pre = self.Ai_model.predict([fast_vec]).argmax()  # 해당 데이터를 인공지능 모델에 적용

            # 해당 comment_info 정보를 label 에 맞춰서 저장
            if test_pre == 0:
                comment_info['label'] = '긍정'
            elif test_pre == 1:
                comment_info['label'] = '부정'
            elif test_pre == 2:
                comment_info['label'] = '악플'

        return comment_list
