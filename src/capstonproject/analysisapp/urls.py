from django.urls import path

from analysisapp.views import AnalysisCreateView, AnalysisListView, AnalysisDetailView

app_name = 'analysisapp'  # 만든것과 이름 똑같이

urlpatterns = [
    path('create/', AnalysisCreateView.as_view(), name='create'),
    path('list/', AnalysisListView.as_view(), name='list'),
    path('detail/<int:pk>', AnalysisDetailView.as_view(), name='detail'),
]
