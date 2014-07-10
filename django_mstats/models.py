import re
from datetime import datetime
from operator import itemgetter

from django.db.models import Count
from django.db import connection
from django.utils import timezone

stats_classes = {}

# Function for converting from InitialCaps to "lowercase with spaces". Taken from Django 1.5
get_verbose_name = lambda class_name: re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', ' \\1', class_name).lower().strip()

# Capitalize first letter of a string
capfirst = lambda s: s[:1].upper() + s[1:]

class StatsMeta(type):
    def __new__(cls, name, bases, dct):
        new = type.__new__(cls, name, bases, dct)
        if not name in ("Stats", "ModelStats"):
            stats_classes[name.lower()] = new()
        return new

class Stats(object):
    name = None
    
    __metaclass__ = StatsMeta
    
    def __init__(self):
        self.key = type(self).__name__.lower

    def get_stats_for_period(self, start_time, stop_time, interval):
        pass
    
    def get_name(self):
        if self.name:
            return self.name
        else:
            return capfirst(get_verbose_name(type(self).__name__))


class ModelStats(Stats):
    model = None
    datetime_field = None
    
    def get_stats_for_period(self, start_time, end_time, interval):
        if not interval in ["hour", "day", "week", "month"]:
            raise ValueError("Valid intervals are: hour, day, week, month")
        
        """
        filters = {}
        filters[self.datetime_field + "__gt"] = start_time
        filters[self.datetime_field + "__lte"] = end_time

        data = [(x["interval"], x["count"]) for x in self.model.objects.filter(**filters).extra({"interval":"date_trunc('" + interval + "', " + self.datetime_field + ")"}).values("interval").annotate(count=Count("pk"))]
        data.sort(key=itemgetter(0))
        return data
        """
        
        tz = timezone.get_current_timezone()
        start_time = timezone.make_aware(start_time, tz)
        end_time = timezone.make_aware(end_time, tz)
        
        # This SQL query is based on the following Stackoverflow answer:
        # http://stackoverflow.com/a/15577413/27406
        sql = """
        WITH vals AS (
           SELECT TIMESTAMP '%(start_time)s'        AS frame_start  -- enter values once
                 ,TIMESTAMP '%(end_time)s'          AS frame_end
                 ,'1 %(interval)s'::interval   AS t_interval
           )
        ,   grid AS (
           SELECT start_time
                 ,lead(start_time, 1, frame_end) OVER (ORDER BY start_time) AS end_time
           FROM   (
              SELECT generate_series(frame_start, frame_end, t_interval) AS start_time
                    ,frame_end
              FROM vals
              ) x
           )
        SELECT to_char(start_time, 'YYYY-MM-DD HH24:MI'), count(tbl.%(dt_field)s) AS events
        FROM   grid       g
        LEFT   JOIN %(table_name)s tbl ON tbl.%(dt_field)s >= g.start_time AND tbl.%(dt_field)s < g.end_time
        GROUP  BY start_time
        ORDER  BY start_time
        """ % {
            "table_name": self.model._meta.db_table, 
            "dt_field": self.datetime_field,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "interval": interval,
        }
        
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()[:-1]
        return [(datetime.strptime(d, "%Y-%m-%d %H:%M"), count) for d, count in rows]

