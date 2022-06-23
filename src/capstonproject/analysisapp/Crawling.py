import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from analysisapp.modelapplication import Model2
import os
from pathlib import Path


class Multi_Crawling:
    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.sad_path = os.path.join(self.BASE_DIR, "sad.pt")
        self.angry_path = os.path.join(self.BASE_DIR, "angry.pt")
        self.anxiety_path = os.path.join(self.BASE_DIR, "anxiety.pt")
        self.wound_path = os.path.join(self.BASE_DIR, "wound.pt")
        self.panic_path = os.path.join(self.BASE_DIR, "panic.pt")
        self.model1_path = os.path.join(self.BASE_DIR, "model1.pt")
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')  # 내부 창을 띄울 수 없으므로 설정
        self.chrome_options.add_argument('--no-sandbox')  # 크롬 실행이 안될때 사용하는 옵션
        self.chrome_options.add_argument('--disable-dev-shm-usage')  # Device 의 shm 디렉토리 를 사용하지 않은 -> shm (공유 디렉토리)
        # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
        self.model2 = Model2(self.sad_path, self.angry_path, self.anxiety_path, self.wound_path, self.panic_path,
                             self.model1_path)

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
                date = date.replace(' ', '')
                date = date.replace('.', '-')
                date = date[:-1]
                Data_list.append({
                    'ID': id,
                    'Comment': comment,
                    'Date': date,
                    'label': self.model2.predict(comment)
                })

        return Data_list
