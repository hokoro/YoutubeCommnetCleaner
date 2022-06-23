from django.db import models, connection


# Create your models here.

class Url(models.Model):
    url1 = models.URLField(max_length=200, null=True, blank=True)
    url2 = models.URLField(max_length=200, null=True, blank=True)
    url3 = models.URLField(max_length=200, null=True, blank=True)
    url4 = models.URLField(max_length=200, null=True, blank=True)
    url5 = models.URLField(max_length=200, null=True, blank=True)
    url6 = models.URLField(max_length=200, null=True, blank=True)


class Comment(models.Model):
    comment = models.TextField(max_length=500, null=False, blank=False)
    author = models.TextField(max_length=20, null=False, blank=False)
    date = models.DateField(auto_now_add=False)
    label = models.CharField(max_length=20, null=False, blank=False)


class Visual(models.Model):
    pie = models.ImageField(upload_to='piechart/', null=False)
    wordcloud = models.ImageField(upload_to='wordcloud/', null=False)
    plot = models.ImageField(upload_to='plotchart/', null=False)
    emotion = models.CharField(max_length=10, null=False, blank=False)
