from django.conf.urls import patterns, include, url

from .views import OverviewView, StatsView, ChartJsView

urlpatterns = patterns('',
    url(r'^$', OverviewView.as_view()),
    url(r'^Chart.js.min$', ChartJsView.as_view(), name="mstats_chart_js"),
    url(r'^(?P<stats_name>[A-z0-9_]+)$', StatsView.as_view(), name="mstats_stats"),
    
)

