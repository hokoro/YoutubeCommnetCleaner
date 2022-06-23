import Youtube
import ModelApplication
import Crawling

# info = Youtube.Youtube()
#
# comment_list = info.get_comments()
#
# print(comment_list)
#
# comment_list = ModelApplication.model1_application('Kor_NLP_LSTM.h5', 'ft_model.bin').model_test(comment_list)
#
# print(comment_list)

url_list = ['https://www.youtube.com/watch?v=6PzT_IurnZw',
            'https://www.youtube.com/watch?v=cFkD1mEaC1Y',
            'https://www.youtube.com/watch?v=X5fbDciuz7A']

m = Crawling.Multi_Crawling()

html_source = m.Crawling(url_list)

Data_List = m.Spelling(html_source)

print(Data_List)

Lstm = ModelApplication.model1_application('Kor_NLP_LSTM.h5', 'ft_model.bin')

comment_list = Lstm.Model_test_demo(Data_List)

df = m.Data_Frame(comment_list)

df.to_csv('MultiCrawling.csv', encoding='utf-8-sig')
