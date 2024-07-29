# Youtube Comment Cleaner

CapStone Design D조 

유튜브 영상속 악플(악성) 댓글 삭제 / 악성 댓글 업데이트 / 크롤링을 통한 감정 시각화 

조원 : 천영성/ 이창현 / 박경서 

## Motivation 

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/zaUukjGhuok/hqdefault.jpg)](https://www.youtube.com/watch?v=zaUukjGhuok)


## Model

### LSTM 
[LSTM (Long Short Term Memory)](https://www.tensorflow.org/api_docs/python/tf/keras/layers/LSTM)는 기존의 RNN이 출력과 먼 위치에 있는 정보를 기억할 수 없다는 단점을 보완하여 장/단기 기억을 가능하게 설계한 신경망의 구조를 말합니다. 주로 시계열 처리나, 자연어 처리에 사용됩니다.
-> 우리 가 사용하는 한글도 한문장 속에서 문장의 처음 부터 끝 까지 의 단어들을 가지고 감정을 파악 해야 하기 때문에 사용 

ACC(Train : 94% / Test: 91%) 

Member : [박경서](https://github.com/unhas01)


### KOBERT
[SKT Brain KoBert Model](https://github.com/SKTBrain/KoBERT) : 한국어 버전의 자연어 처리 모델 
기존 BERT 에서 한국어 데이터 셋으로 연구해 한국어 에 더 적합 한 모델 
구조는 기존의 BERT 와 마찬가지로 텍스트 를 양방향 앞뒤 확인 하여 자연어 처리 하는 모델이다 
기존의 자연어 처리 모델은 단방향 우리가 글을 읽는 순서인 왼쪽→오른쪽으로 갔지만 BERT는 이 순서를 양방향으로 보기 때문에 다른 모델에 비해 매우 높은 정확도를 나타낸다. 

KOBERT 는 기존의 BERT 를 한국어 형 버전으로 만든 모델이다 

ACC(Train: 87%/ Test: 68%)

Member : [이창현](https://github.com/changhyun0327)

### KCELECTRA 
모델 학습을 시작하기 전에 파인튜닝에 사용될 KcELECTRA 에 대해 간단하게 알아보자. [KcELECTRA](https://github.com/Beomi/KcELECTRA) 는 이전 에어프로젝트에서 사용한 KoBERT 와 마찬가지로 한국어 데이터를 활용해 학습시킨 모델로 다중언어로 학습된 모델보다 한국어 처리에 대해 훨씬 뛰어난 성능을 보인다. 

1.데이터 가 일반 문장과 다르게 실제 기사의 뉴스 댓글등이 많아서 훨씬더 좋은 성능을 보인다 

2.학습의 모델 구조가 다르다 
Generator를 통해 다소 그럴 듯한 가짜 토큰으로 대체하는 방식으로 입력된 문장을 변형시킨다. 

model 1 = (Train:99%  / Test:96%)

sad,angry,anxiety,wound,panic = (Train:98% / Test: 93%)

Member : [천영성](https://github.com/hokoro)

## Data visualization 
수집한 댓글을 가지고 원형 차트 , 시계열 별 데이터 수를 보여주는 직선 차트 , 워드 클라우드 , 가장 많이 분석된 감정들을 시각화 

[PIE](https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_features.html)

<img src="http://sw-git.chosun.ac.kr/ycc/ycc/-/raw/main/Data/Image/piechart13.jpg" width="30%" height="30%">

[WordCloud](https://amueller.github.io/word_cloud/)


<img src="http://sw-git.chosun.ac.kr/ycc/ycc/-/raw/main/Data/Image/wordcloud13.jpg" width="30%" height="30%">


[Time Series Plot Chart](https://matplotlib.org/stable/gallery/index.html)


<img src="http://sw-git.chosun.ac.kr/ycc/ycc/-/raw/main/Data/Image/plotchart13.jpg" width="30%" height="30%">

Max_Emotion 추출

<img src="http://sw-git.chosun.ac.kr/ycc/ycc/-/raw/main/Data/Image/%EA%B0%90%EC%A0%95.PNG" width="30%" height="30%">

Member : [박경서](https://github.com/unhas01)

## Data 

[AI HUB 단발성 대화 데이터 셋](https://aihub.or.kr/opendata/keti-data/recognition-laguage/KETI-02-009)

[한국어 욕설 데이터 셋](https://github.com/2runo/Curse-detection-data)

[스마일게이트 데이터 셋](https://github.com/smilegate-ai/korean_unsmile_dataset)



Member

[박경서](https://github.com/unhas01)

[이창현](https://github.com/changhyun0327)


## Web 
<img src="http://sw-git.chosun.ac.kr/ycc/ycc/-/raw/main/Data/Image/%EB%A9%94%EC%9D%B8_%ED%8E%98%EC%9D%B4%EC%A7%80.png" width="45%" height="45%">


FrontEnd : [HTML , CSS , JS](https://poiemaweb.com/) , [BootStrap4](https://getbootstrap.com/docs/4.6/getting-started/introduction/)

Backend : [Django(Python)](https://www.djangoproject.com/)

API : [Youtube API Data V3](https://developers.google.com/youtube/v3/getting-started?hl=ko)


Setting , FrontEnd: [이창현](https://github.com/changhyun0327)

API , Backend: [천영성](https://github.com/hokoro)




