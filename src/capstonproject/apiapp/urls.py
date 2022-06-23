from django.urls import path

from apiapp.views import GoogleOauth, GoogleLoginView, VideoListView, Comment_Post, CommentListView, CommentUpdate, \
    CommentDelete

app_name = 'apiapp'  # 만든것과 이름 똑같이

urlpatterns = [
    path('', GoogleOauth, name='oauth'),
    path('code/', GoogleLoginView.as_view(), name='Login'),
    path('list/', VideoListView.as_view(), name='list'),
    path('comment/<str:video_id>', Comment_Post, name='video'),
    path('commentlist/', CommentListView.as_view(), name='comment'),
    path('update/', CommentUpdate, name='update'),
    path('delete/', CommentDelete, name='delete'),
]
