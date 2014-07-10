import os
import json
from datetime import datetime, timedelta

from django.conf import settings
from django.http import Http404, HttpResponse
from django.utils.importlib import import_module
from django.views import generic

from .models import stats_classes

DATE_FORMAT = "%Y-%m-%d %H:%M"

def import_stats_modules():
    for app in settings.INSTALLED_APPS:
        try:
            import_module("%s.mstats" % app)
        except ImportError:
            #print "got import error"
            pass
        else:
            #print "imported %s.mstats" % app
            pass


class OverviewView(generic.TemplateView):
    template_name = "mstats/overview.html"
    
    def get_context_data(self):
        import_stats_modules()
        return {
            "stats_classes": stats_classes.values(),
        }
    
class StatsView(generic.TemplateView):
    template_name = "mstats/stats.html"
    
    def get_context_data(self, stats_name):
        import_stats_modules()
        try:
            stats = stats_classes[stats_name]
        except KeyError:
            raise Http404("Stats not found")
        
        interval = self.request.GET.get("interval", "day")
        if not interval in ("hour", "day", "week", "month"):
            raise Http404("Wrong interval")
        
        start_time = self.request.GET.get("start_time")
        stop_time = self.request.GET.get("stop_time")
        
        if start_time or stop_time:
            start_time = datetime.strptime(start_time, DATE_FORMAT)
            stop_time = datetime.strptime(stop_time, DATE_FORMAT)
        
        if interval == "hour":
            label_format = "%H:%M"
            if not start_time or not stop_time:
                stop_time = datetime.now() + timedelta(hours=1)
                stop_time = stop_time.replace(minute=0, second=0, microsecond=0)
                start_time = stop_time - timedelta(hours=24)
        elif interval == "day":
            label_format = "%b %d"
            if not start_time or not stop_time:
                stop_time = datetime.now() + timedelta(days=1)
                stop_time = stop_time.replace(hour=0, minute=0, second=0, microsecond=0)
                start_time = stop_time - timedelta(days=30)
        elif interval == "week":
            label_format = "%b %d"
            if not start_time or not stop_time:
                stop_time = datetime.now() + timedelta(days=1)
                stop_time = stop_time.replace(hour=0, minute=0, second=0, microsecond=0)
                start_time = stop_time - timedelta(days=175)
        elif interval == "month":
            label_format = "%b %Y"
            if not start_time or not stop_time:
                stop_time = datetime.now() + timedelta(days=31)
                stop_time = stop_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                start_time = stop_time - timedelta(days=365)
        
        stats_data = stats.get_stats_for_period(start_time, stop_time, interval)
        #print "stats:", stats_data
        
        labels = [dt.strftime(label_format) for dt, _ in stats_data]
        values = [val for _, val in stats_data]
        
        return {
            "stats": stats,
            "labels": json.dumps(labels),
            "values": json.dumps(values),
            "interval": interval,
            "intervals": [("hour","Hourly"), ("day","Daily"), ("week","Weekly"), ("month","Monthly")],
            "start_time": start_time.strftime(DATE_FORMAT),
            "stop_time": stop_time.strftime(DATE_FORMAT),
        }

class ChartJsView(generic.View):
    def get(self, request):
        with file(os.path.join(os.path.abspath(os.path.dirname(__file__)), "static", "Chart.min.js")) as f:
            data = f.read()
        return HttpResponse(data, content_type="application/javascript")
