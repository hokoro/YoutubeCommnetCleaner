'''
유튜브 크롤링 기능 구현
'''
import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class Single_Crawling:
    def __init__(self, url):
        self.user_IDS_list = []  # 해당 유저의 ID
        self.user_comments_list = []  # 해당 유저가 쓴 Comment
        self.url = url
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')  # 내부 창을 띄울 수 없으므로 설정
        self.chrome_options.add_argument('--no-sandbox')  # 크롬 실행이 안될때 사용하는 옵션
        self.chrome_options.add_argument('--disable-dev-shm-usage')  # Device 의 shm 디렉토리 를 사용하지 않은 -> shm (공유 디렉토리)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)

    def Crawling(self):
        self.driver.get(self.url)  # 해당 url 의 정보를 chrome driver 에 저장
        last_page_height = self.driver.execute_script(
            "return document.documentElement.scrollHeight")  # 현재 스크롤 페이지 의 높이 를 지정
        while True:
            self.driver.execute_script(
                "window.scrollTo(0, document.documentElement.scrollHeight);")  # scrollTo 를 이용해 맨 위에서 부터 스크롤 시작
            time.sleep(3.0)  # 스크롤을 내리고 페이지가 뜨는 시간을 계산 -> 수정 예정
            new_page_height = self.driver.execute_script(
                "return document.documentElement.scrollHeight")  # 스크롤이 내려가면 새로운 페이지의 높이를 다시 지정
            if new_page_height == last_page_height:  # 해당 페이지가 스크롤이 더이상 내려가지 않을경우
                break
            last_page_height = new_page_height  # 현재 페이지 의 높이를 마지막 높이로 지정
        html_source = self.driver.page_source  # 스크롤을 내리면서 가져온 html 정보를 저장
        self.driver.close()  # Driver 종료

        soup = BeautifulSoup(html_source, 'lxml')  # html 파일을 lxml 형식으로 Bs 시작

        youtube_user_IDs = soup.select('#author-text > span')  # 유저의 ID 부분
        youtube_comments = soup.select('#content-text')  # 유저의 작성한 댓글
        youtube_upload_date = soup.select('#info-strings > yt-formatted-string')  # 해당 영상의 업로드 날짜

        return youtube_user_IDs, youtube_comments, youtube_upload_date

    def Spelling(self, user_IDs, user_Comments):  # 해당 댓글들의 줄바꿈 / tab / 스페이스 바 들을 replace 통해 변경
        for i in range(len(user_IDs)):
            str_tmp = str(user_IDs[i].text)
            str_tmp = str_tmp.replace('\n', '')
            str_tmp = str_tmp.replace('\t', '')
            str_tmp = str_tmp.replace('               ', '')
            str_tmp = str_tmp.strip()
            self.user_IDS_list.append(str_tmp)

            str_tmp = str(user_Comments[i].text)
            str_tmp = str_tmp.replace('\n', '')
            str_tmp = str_tmp.replace('\t', '')
            str_tmp = str_tmp.replace('               ', '')
            str_tmp = str_tmp.strip()
            self.user_comments_list.append(str_tmp)

        return self.user_IDS_list, self.user_comments_list

    def DataFrame(self, date):  # 해당 정보들의 DataFrame 화 시켜 return
        comment_data = {'ID': self.user_IDS_list, 'Comment': self.user_comments_list, 'Date': date}
        youtube_df = pd.DataFrame(comment_data)

        return youtube_df


class Multi_Crawling:
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')  # 내부 창을 띄울 수 없으므로 설정
        self.chrome_options.add_argument('--no-sandbox')  # 크롬 실행이 안될때 사용하는 옵션
        self.chrome_options.add_argument('--disable-dev-shm-usage')  # Device 의 shm 디렉토리 를 사용하지 않은 -> shm (공유 디렉토리)
        # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)

    def Crawling(self, url_list):
        html_source_list = []

        for url in url_list:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
            driver.get(url)

            last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

            while True:
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                time.sleep(3.0)
                new_page_height = driver.execute_script("return document.documentElement.scrollHeight")

                if new_page_height == last_page_height:
                    break
                last_page_height = new_page_height

            html_source = driver.page_source
            html_source_list.append(html_source)
            print(url, "Complete!")

            driver.quit()
        return html_source_list

    def Spelling(self, html_source_list):
        Data_list = []

        for html in html_source_list:
            soup = BeautifulSoup(html, 'lxml')

            youtube_user_IDs = soup.select('#author-text > span')  # 유저의 ID 부분
            youtube_comments = soup.select('#content-text')  # 유저의 작성한 댓글
            youtube_upload_date = soup.select('#info-strings > yt-formatted-string')  # 해당 영상의 업로드 날짜

            for i in range(len(youtube_user_IDs)):
                id = str(youtube_user_IDs[i].text)
                id = id.replace('\n', '')
                id = id.replace('\t', '')
                id = id.replace('                ', '')
                id = id.strip()

                comment = str(youtube_comments[i].text)
                comment = comment.replace('\n', '')
                comment = comment.replace('\t', '')
                comment = comment.replace('                ', '')
                comment = comment.strip()

                date = youtube_upload_date[0].text
                Data_list.append({
                    'ID': id,
                    'Comment': comment,
                    'Date': date,
                    'label': None
                })

        return Data_list

    def Data_Frame(self, Data_list):
        df = pd.DataFrame(Data_list)
        print(df.isnull().sum())

        df = df.dropna(axis=0)

        return df



