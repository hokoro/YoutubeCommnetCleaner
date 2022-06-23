from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView

# Create your views here.
import analysisapp.models
import apiapp.models
from analysisapp.models import *
from apiapp.models import *


def mainpage(request):
    C1 = analysisapp.models.Comment.objects.all()
    C2 = apiapp.models.Comment.objects.all()
    V = apiapp.models.Video.objects.all()
    V.delete()
    C1.delete()
    C2.delete()
    return render(request, 'capstonapp/mainpage.html')


# class UrlCreateView(CreateView):
#     model = Url
#     form_class = UrlCreateForm
#     template_name = 'capstonapp/mainpage.html'
#
#     def get_success_url(self):
#         return reverse('capstonapp:create')
