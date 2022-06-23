import pandas as pd
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
from pathlib import Path


class Visualization:
    def __init__(self, comment, label, data):
        # word cloud member variable
        self.comment = comment
        self.word_count = dict()
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.NanumGothic = os.path.join(self.BASE_DIR, "NanumGothic.ttf")
        # Pie chart member variable
        self.series = pd.Series(data=label)
        self.label = ['Happy', 'Sad', 'Angry', 'Anxiety', 'Wound', 'Panic', 'Abuse', 'No Meaning']
        self.ratio_dict = {'기쁨': 0, '슬픔': 0, '분노': 0, '불안': 0, '상처': 0, '당황': 0, '욕설': 0, '무의미': 0}
        self.ratio_list = list(self.series.value_counts().index)
        for ratio in self.ratio_list:
            self.ratio_dict[ratio] = self.series.value_counts()[ratio]
        self.ratio = list(self.ratio_dict.values())
        self.explode = []

        # Time Series plot chart
        self.df = pd.DataFrame(data=data, columns=['date', 'label'])
        self.x = list(set(self.df['date'])).sort()
        print(self.x)
        self.label_set = list(set(self.df['label']))
        self.label_dict = {'기쁨': 'Happy', '슬픔': 'Sad', '분노': 'Angry', '불안': 'Anxiety',
                           '상처': 'Wound', '당황': 'Panic', '욕설': 'Abuse', '무의미': 'No Meaning'}

    def Max_label(self):
        list_of_key = list(self.ratio_dict.keys())
        list_of_value = list(self.ratio_dict.values())

        position = list_of_value.index(max(self.ratio_dict.values()))

        return list_of_key[position]

    # Word Cloud Member Function
    def WordCloud_Processing(self):
        message = ''
        for item in self.comment:
            message = message + str(item)

        nlp = Okt()
        message_N = nlp.nouns(message)  # 명사로 추출
        count = Counter(message_N)  # Count값 계산

        for tag, counts in count.most_common(80):  # word_count(딕셔너리)에 2단어 이상만 저장
            if len(str(tag)) > 1:
                self.word_count[tag] = counts

    def WordCloud(self, visual_id):
        base_route = 'media/wordcloud/'
        wc = WordCloud(self.NanumGothic, background_color='ivory', width=800,
                       height=600)  # !!!!!!!글꼴 설정 부분!!!!!!!!!!!
        cloud = wc.generate_from_frequencies(self.word_count)
        plt.figure(figsize=(16, 16))
        plt.imshow(cloud)
        plt.axis('off')
        plt.title('WordCloud')
        plt.savefig(fname=base_route + 'wordcloud' + str(visual_id) + '.jpg', bbox_inches='tight')
        plt.show()
        save_route = 'wordcloud/wordcloud' + str(visual_id) + '.jpg'
        return save_route

    # Pie Chart Member Function

    def Set_explode(self):
        for i in range(len(self.label)):
            self.explode.append(0.08)

    def Pie(self, visual_id):
        base_route = 'media/piechart/'
        # plt.rc('font', family=font_name)  # !!!!!!!글꼴 설정 부분!!!!!!!!!!!
        wed = {'edgecolor': 'black', 'linewidth': 1.5}
        plt.figure(figsize=(20, 20))
        plt.title('Pie Chart')
        plt.pie(self.ratio, labels=self.label, autopct='%.1f%%', explode=self.explode, shadow=True, wedgeprops=wed
                , textprops={'fontsize': 20})
        plt.legend(loc=(1, 0.5))
        plt.savefig(fname=base_route + 'piechart' + str(visual_id) + '.jpg', bbox_inches='tight')
        plt.show()
        save_route = 'piechart/piechart' + str(visual_id) + '.jpg'

        return save_route

    # Time Series Plot chart Member Function
    def Line(self, visual_id):
        base_route = 'media/plotchart/'
        plt.figure(figsize=(10, 10))
        # plt.rc('font', family=font_name)
        plot_df = self.df.groupby(['date', 'label']).size().unstack(fill_value=0)
        plt.title('Time Series Plot Chart')
        plt.xlabel('Date')
        plt.ylabel('Count')
        for label in self.label_set:
            plt.plot(plot_df[label], marker='o', label=self.label_dict[label])
            # plt.plot(self.x, plot_df[label], marker='o', linestyle='--', label=self.label_dict[label])
            plt.legend()
        plt.grid()
        plt.xticks(rotation=20)
        plt.savefig(fname=base_route + 'plotchart' + str(visual_id) + '.jpg', bbox_inches='tight')
        plt.show()
        save_route = 'plotchart/plotchart' + str(visual_id) + '.jpg'

        return save_route
