from django.db import models


# Create your models here.


class AccessToken(models.Model):
    accesstoken = models.CharField(max_length=30, null=False)


class Video(models.Model):
    video_id = models.CharField(max_length=20, null=False, blank=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    date = models.DateField(auto_now_add=False)


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, related_name='comment', null=True)
    comment_id = models.CharField(max_length=30, null=False, blank=False)
    comment = models.TextField(max_length=500, null=False, blank=False)
    author = models.CharField(max_length=30, null=False, blank=True)
    comment_date = models.DateField(auto_now_add=False)
    label = models.CharField(max_length=15, null=False, blank=False)
