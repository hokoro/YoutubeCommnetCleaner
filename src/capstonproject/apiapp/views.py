import json

from django.shortcuts import render, redirect

import requests
# Create your views here.
from django.views import View
from django.views.generic import ListView

# from apiapp.forms import ApiCreationForm


from apiapp.fix import Preprocessing
from apiapp.models import Video
from apiapp.models import Comment
from apiapp.models import AccessToken
from capstonproject import settings
from apiapp.modelapplication import Model1
import os
from pathlib import Path


def GoogleOauth(request):
    scope = ['https://www.googleapis.com/auth/youtube.readonly',
             'https://www.googleapis.com/auth/youtube.force-ssl']

    client_id = settings.GOOGLE_CLIENT_ID
    redirect_url = settings.GOOGLE_REDIRECT_URL_ENCODING

    google_auth_api = 'https://accounts.google.com/o/oauth2/auth'

    V = Video.objects.all()
    V.delete()

    return redirect(
        f"{google_auth_api}?client_id={client_id}&redirect_uri={redirect_url}&scope={scope[0]} {scope[1]}&response_type=code&access_type=offline")


class GoogleLoginView(View):
    def get(self, request):
        google_access_code = request.GET.get('code', None)
        client_id = settings.GOOGLE_CLIENT_ID
        redirect_url = settings.GOOGLE_REDIRECT_URL
        secret_key = settings.GOOGLE_SECRET_KEY

        url = 'https://accounts.google.com/o/oauth2/token'

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        body = {
            'code': f'{google_access_code}',
            'client_id': client_id,
            'client_secret': secret_key,
            'redirect_uri': redirect_url,
            'grant_type': 'authorization_code',
        }

        google_response = requests.post(url=url, headers=headers, data=body)
        google_response_dict = json.loads(google_response.text)
        # print(google_response_dict['access_token'])
        # return render(request, 'apiapp/token.html', {'access_token': google_response.text})
        # google_response_dict = json.loads(google_response.text)
        token = google_response_dict['access_token']
        A = AccessToken(accesstoken=token)
        A.save()

        url = f'https://www.googleapis.com/youtube/v3/channels?part=contentDetails&mine=true&access_token={token}'

        channel_response = requests.get(url)
        channel_information = json.loads(channel_response.text)
        channel_id = channel_information['items'][0]['contentDetails']['relatedPlaylists']['uploads']
       


        url = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={channel_id}&key={api_key}'
        video_response = requests.get(url)
        video_information = json.loads(video_response.text)
        upload_video_len = video_information['pageInfo']['totalResults']

        comment_list = []
        for i in range(upload_video_len):
            video_date = video_information['items'][i]['snippet']['publishedAt'][:10]
            video_id = video_information['items'][i]['snippet']['resourceId']['videoId']
            video_title = video_information['items'][i]['snippet']['title']

            video_object = Video(video_id=video_id, title=video_title, date=video_date)
            video_object.save()

        # return HttpResponse(f'{video_response.text}')
        return render(request, 'apiapp/token.html')


class VideoListView(ListView):
    model = Video
    context_object_name = 'video_list'
    template_name = 'apiapp/video_list.html'
    paginate_by = 20

    def get_queryset(self):
        C = Comment.objects.all()
        C.delete()
        video_list = Video.objects.all().order_by('date')
        return video_list


def Comment_Post(request, video_id):
    BASE_DIR = Path(__file__).resolve().parent.parent
    model1_path = os.path.join(BASE_DIR, 'model1.pt')
    model1 = Model1(model1_path)
    video = Video.objects.filter(video_id=video_id)
    max_result = 100
    url = f'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults={max_result}' \
          f'&textFormat=plainText&videoId={video_id}&key={api_key}'
    comment_response = requests.get(url)
    comment_information = json.loads(comment_response.text)
    for comment_info in comment_information['items']:
        comment_id = comment_info['id']
        comment = comment_info['snippet']['topLevelComment']
        author = comment['snippet']['authorDisplayName']
        comment_date = comment['snippet']['publishedAt'][:10]
        text = comment['snippet']['textDisplay']
        label = model1.predict(text)

        comment_object = Comment(comment_id=comment_id, comment=text, author=author, comment_date=comment_date,
                                 label=label, video=Video.objects.get(video_id=video_id))

        comment_object.save()

    comment_list = Comment.objects.all().order_by('comment_date')
    return render(request, 'apiapp/comment_list.html', {'comment_list': comment_list, 'video_id': video_id})


class CommentListView(ListView):
    model = Comment
    context_object_name = 'comment_list'
    template_name = 'apiapp/comment_list.html'
    paginate_by = 20

    def get_queryset(self):
        comment_list = Comment.objects.all().order_by('comment_date')
        return comment_list


def CommentUpdate(request):
    BASE_DIR = Path(__file__).resolve().parent.parent
    badword_a_path = os.path.join(BASE_DIR,'badword-A.txt')
    badword_b_path = os.path.join(BASE_DIR,'badword-B.txt')
    token_count = AccessToken.objects.count()
    token = AccessToken.objects.get(pk=token_count)
    comment_fix = Preprocessing(badword_a_path, badword_b_path)

    url = f'https://youtube.googleapis.com/youtube/v3/comments?part=snippet&key={api_key}'

    headers = {
        'Authorization': f'Bearer {token.accesstoken}',
        'Accept': 'application / json',
        'Content-Type': 'application/json',
    }

    queryset = Comment.objects.all()

    for comment_data in queryset:
        comment = comment_data.comment

        # comment 맞춤법 수정
        comment = comment_fix.Bad_Word_Convert(comment)
        comment = comment_fix.Spell_Checker(comment)
        comment = comment_fix.Spacing(comment)

        body = {
            'id': comment_data.comment_id,
            'snippet': {
                "textOriginal": comment
            }
        }
        update_response = requests.put(url=url, headers=headers, data=json.dumps(body))

        comment_data.comment = comment
        comment_data.save()

    comment_list = Comment.objects.all().order_by('comment_date')
    return render(request, 'apiapp/update.html', {'comment_list': comment_list})


def CommentDelete(request):
    queryset = Comment.objects.all()
    token_count = AccessToken.objects.count()
    token = AccessToken.objects.get(pk=token_count)

    headers = {
        'Authorization': f'Bearer {token.accesstoken}',
        'Accept': 'application/json'
    }
    for comment_data in queryset:
        if comment_data.label == '악플':
            url = f'https://youtube.googleapis.com/youtube/v3/comments?id={comment_data.comment_id}&key={api_key}'
            requests.delete(url=url, headers=headers)
            Comment.objects.filter(comment=comment_data.comment).delete()

    comment_list = Comment.objects.all().order_by('comment_date')
    return render(request, 'apiapp/delete.html', {'comment_list': comment_list})
