from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
# from .views import APITestView

from Dashboard.views import DashboardView
from RawData.views import *
from MachineLearning.views import MachineLearningResultView, APIMachineLearningAccuracy


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # Dashboard
    url(r'^$', DashboardView.as_view(), name='dashboard'),

    # Raw Data View
    url(r'^RawData/event-flow/$', RawDataEventFlowView.as_view(), name='raw-data-event-flow'),
    url(r'^RawData/data-trend/$', RawDataDataTrendView.as_view(), name='raw-data-data-trend'),
    # Raw Data API
    url(r'^api/RawData/event-flow/$', APIRawDataEventFlowView.as_view(), name='api-raw-data-event-flow'),
    url(r'^api/RawData/data-trend/$', APIRawDataDataTrendView.as_view(), name='api-raw-data-data-trend'),

    # Machine Learning
    url(r'^MachineLearning/ML-result/$', MachineLearningResultView.as_view(), name='machine-learning-result'),
    url(r'^api/MachineLearning/accuracy/$', APIMachineLearningAccuracy.as_view(), name='machine-learning-accuracy'),

    # chart view: for testing purpose
    url(r'^RawData/event-flow-chart/$', RawDataEventFlowChartView.as_view(), name='raw-data-event-flow-chart'),

    # API
    # url(r'^api/test/$', APITestView.as_view(), name='api-test'),
    url(r'^api/rawdata/event-flow-data/$', APIRawDataEventFlowData.as_view(), name='api/rawdata/event-flow-data'),
    url(r'^api/ml/prediction-data/$', APIRawDataEventFlowData.as_view(), name='api/ml/prediction-data'),

    # Developing
    #url(r'^RawData/event-flow-chart/demo$', RawDataEventFlowChartView.as_view(), name='raw-data-event-flow-chart-demo'),
    url(r'^django_angular_demo$', django_angular_demo.as_view(), name='django_angular_demo'),



]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)