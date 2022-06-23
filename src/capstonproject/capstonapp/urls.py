from django.urls import path


from capstonapp.views import mainpage

app_name = 'capstonapp' #만든것과 이름 똑같이

urlpatterns =[
    path('mainpage/',mainpage,name='mainpage')
]