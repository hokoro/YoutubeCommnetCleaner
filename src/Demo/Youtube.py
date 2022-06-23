import google_auth_oauthlib.flow
import googleapiclient.discovery


class Youtube:
    def __init__(self):
        self.API_SERVICE_NAME = 'youtube'  # api 서비스 이름
        self.API_VERSION = 'v3'  # 현재 api 서비스 이름은 youtube api Data v3
        self.CLIENT_SECRET_FILE = 'client_secret.json'  # api json data file

        # APPS = api 로 사용할수 있는 기능 1.자신의 계정의 영상 탐색 , YouTube 동영상, 평가, 댓글, 자막 보기, 수정 및 완전 삭제
        self.APPS = ['https://www.googleapis.com/auth/youtube.readonly',
                     'https://www.googleapis.com/auth/youtube.force-ssl']

        # api 객체를 얻어 계정 인증 및 credential 실행
        self.flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(self.CLIENT_SECRET_FILE,
                                                                                        self.APPS)
        self.credentials = self.flow.run_console()
        self.youtube = googleapiclient.discovery.build(self.API_SERVICE_NAME, self.API_VERSION,
                                                       credentials=self.credentials)

        # 영상속 댓글들의 정보 영상
        self.comment_list = []

        # 삭제할 댓글의 작성자의 채널 ID info_list
        self.comment_delete_list = []
        self.comment_delete_info_list = []

        # 복구할 댓글의 작성자의 채널 ID list
        self.comment_restoration_list = []
        # 댓글 작성자 차단 여부
        self.banned = None
        # 인증된 계정의 정보 가져오기
        self.channels_response = self.youtube.channels().list(
            mine=True,
            part='contentDetails'
        ).execute()

        # 사용자 계정의 채널 id 가져오기
        '''
        https://www.youtube.com/channel/UC0KWgy6ZtS6Ex4lsarwgl7A
        uploads_playlist_id = UC0KWgy6ZtS6Ex4lsarwgl7A
        '''
        self.channel = self.channels_response['items'][0]
        self.uploads_playlist_id = self.channel['contentDetails']['relatedPlaylists']['uploads']

        # 인증된 사용자 채널의 모든 비디오 정보 가져오기
        self.playlistitems_list_request = self.youtube.playlistItems().list(
            playlistId=self.uploads_playlist_id,
            part='snippet',
            maxResults=50
        )
        # 비디오 정보를 담고 있는 리스트
        self.video_list = []

        # 해당 플레이 리스트의 모든 동영상을 하나씩 확인하며
        while self.playlistitems_list_request:
            self.playlistitems_list_response = self.playlistitems_list_request.execute()

            # 각 비디오(video)에 대한 정보 출력
            for playlist_item in self.playlistitems_list_response['items']:
                video_id = playlist_item['snippet']['resourceId']['videoId']
                title = playlist_item['snippet']['title']
                self.video_list.append((video_id, title))

            self.playlistitems_list_request = self.youtube.playlistItems().list_next(self.playlistitems_list_request,
                                                                                     self.playlistitems_list_response)

    def get_comments(self):
        print('댓글을 가지고 오고 싶은 영상을 선택 하세요')
        for playlist_info in self.video_list:
            print('--------------------------------------')
            print('video_id: ', playlist_info[0])  # 해당 Video id 정보
            print('video_title', playlist_info[1])  # 해당 video 의 제목
        print('--------------------------------------')
        video_id = input('위에 정보중 video id 를 입력하세요')

        comment_result = self.youtube.commentThreads().list(  # 해당 비디오 의 모든 정보를 가져오는 스레드
            part='snippet',  # snippet 개체는 동영상의 제목, 설명, 카테고리 등 동영상에 대한 기본 세부정보를 포함합니다.
            videoId=video_id,  # video id
            textFormat='plainText',  # 댓글 수집 의 형식 지정 ( 1. html 문서 형식 / 2. 기본 text plain text 형식)
            maxResults=100,  # 확인하고 싶은 댓글의 수
        ).execute()

        for comment_info in comment_result['items']:
            comment_id = comment_info['id']   # 댓글 작성자의 아이디  = 채널의 고유 아이디 (ex) UC0KWgy6ZtS6Ex4lsarwgl7A)
            comment = comment_info['snippet']['topLevelComment']  # 사용자가 작성한 댓글 의 정보 ( 작성자의 구글 이름 / 작성한 댓글 / 작성한 날짜 )
            author = comment['snippet']['authorDisplayName']  # 작성자의 구글 이름 (천영성)
            publishedAt = comment['snippet']['publishedAt']  # 작성한 댓글의 날짜
            text = comment['snippet']['textDisplay']  # 작성자 가 작성한 댓글
            self.comment_list.append({   # 해당 정보를 list 안에 하나의 딕셔너리 형태로 저장
                'comment_id': comment_id,
                'author': author,
                'publishedAt': publishedAt,
                'text': text,
                'label': None  # 해당 댓글을 model 에 적용 했을때 결과 를 출력
            })

        return self.comment_list  # 해당 comment list 를 return

    def comment_delete(self):  # model label 이 악플일 경우 자동 삭제
        for comment_info in self.comment_list:
            if comment_info['label'] == '악플':
                self.comment_delete_info_list.append({'comment_id': comment_info['comment_id'],
                                                      'author': comment_info['author'],
                                                      'text': comment_info['text'],
                                                      'label': comment_info['label'],
                                                      })
                self.comment_delete_list.append(comment_info['comment_id'])

        self.banned = True
        comment_request = self.youtube.comments().delete(
            id=self.comment_delete_list,
        )
        comment_request.execute()

    def comment_restoration(self):  # model 오류시 댓글 복구
        for comment_info in self.comment_delete_info_list:
            print(f"Comment_id:{comment_info['comment_id']}/ Author:{comment_info['author']}/ Text:{comment_info['text']}")
            restoration_choice = input('해당 댓글이 label 이 잘못 나왔다고 판단 되면 복구 하셔도 됩니다(복구 : 1 / 복구하지 않음 : 0): ')
            if restoration_choice == 1:
                self.comment_restoration_list.append(comment_info['comment_id'])
            else:
                continue

        self.banned = False

        comment_request = self.youtube.comments().setModerationStatus(
            id=self.comment_restoration_list,
            moderationStatus='published',
            banAuthor=self.banned
        )
        comment_request.execute()

# info = Youtube()
# print(info.get_comments())
# print(info.comment_list[0]['label'])
