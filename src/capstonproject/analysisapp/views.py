# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView

from analysisapp import Crawling, Visualization
from analysisapp.forms import AnalysisCreationForm
from analysisapp.models import Url, Comment, Visual


class AnalysisCreateView(CreateView):
    model = Url
    form_class = AnalysisCreationForm
    template_name = 'analysisapp/create.html'

    def get_success_url(self):
        column_name = ['url1', 'url2', 'url3', 'url4', 'url5', 'url6']
        url_count = self.model.objects.count()
        url_model = self.model.objects.filter(id=url_count)

        url_list = url_model.values('url1', 'url2', 'url3', 'url4', 'url5', 'url6')
        final_url_list = []
        for column in column_name:
            if not url_list[0][column]:
                continue
            else:
                final_url_list.append(url_list[0][column])
        # multicrawling
        Crawl = Crawling.Multi_Crawling()
        html_source_list = Crawl.Crawling(url_list=final_url_list)
        Data_list = Crawl.Spelling(html_source_list=html_source_list)

        for Data in Data_list:
            c = Comment(comment=Data['Comment'], author=Data['ID'], date=Data['Date'], label=Data['label'])
            c.save()

        # Member Variable setting
        comment = Comment.objects.values_list('comment', flat=True)
        date = Comment.objects.values_list('date', flat=True).order_by('date')
        label = Comment.objects.values_list('label', flat=True).order_by('date')

        data = {'date': date, 'label': label}

        # Initial
        Visual_object = Visualization.Visualization(comment=comment, label=label, data=data)

        # Max Emotion
        Max_label = Visual_object.Max_label()

        # Word cloud
        Visual_object.WordCloud_Processing()
        wc_route = Visual_object.WordCloud(visual_id=url_count)

        # Pie Chart
        Visual_object.Set_explode()
        pie_route = Visual_object.Pie(visual_id=url_count)

        # Time Series Plot
        plot_route = Visual_object.Line(visual_id=url_count)

        V = Visual(pie=pie_route, wordcloud=wc_route, plot=plot_route, emotion=Max_label)
        V.save()

        return reverse('analysisapp:detail', kwargs={'pk': Visual.objects.count()})


class AnalysisDetailView(DetailView):
    model = Visual
    context_object_name = 'target_visual'
    template_name = 'analysisapp/detail.html'


class AnalysisListView(ListView):
    model = Comment
    context_object_name = 'comment_list'
    template_name = 'analysisapp/list.html'
    paginate_by = 100

    def get_queryset(self):
        comment_list = Comment.objects.all().order_by('date')
        return comment_list
