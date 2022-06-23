from django.forms import ModelForm

from analysisapp.models import Url


class AnalysisCreationForm(ModelForm):
    class Meta:
        model = Url
        fields = ['url1','url2','url3','url4','url5','url6']