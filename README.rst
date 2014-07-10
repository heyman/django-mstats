=============
Django MStats
=============

**Please note**: *Django MStats is in early development and the API is very likely to change.*

MStats is a super simple, re-usable, stateless Django app for visualizing and browsing statistics, mainly 
based on existing Django models.

My motivation for creating MStats is to have a dead simple way, with as little effort as possible, to get 
visualization of key metrics in different Django projects. 

The goal of Django MStats is *not* to be the ultimate metrics/statistics solution™. It will not support 
different backends for different Metrics services and databases. MStats makes all queries in real-time, 
and does not store any permanent data itself, even though Django's cache might be used.

In other words, Django MStats is a reusable app for those who want to get basic statistics browsing with 
minimum effort. Since MStats is stateless, it can easily be tested out, and thrown away in favor of 
something more advanced, if a project grow out of it.


What does M in Mstats stand for?
================================

Model or Mini. Whichever you like best.


Requirements
============

Currently MStats depends on PostgreSQL, because it uses a Postgres specific SQL functions for retrieving 
stats. 


Installation
============

1. Install from PyPI::

    pip install django-mstats

2. Add django_mstats to INSTALLED_APPS

3. Add URL route to your urls.py::

    url(r"^mstats/", include("django_mstats.urls")),

4. Create **mstats.py** file(s) in your Django apps (see below).


Defining different metrics
==========================

Once you have added django_mstats to your INSTALLED_APPS, you can create mstats.py files within your 
Django apps. In those files you should create classes that inherits from ModelStats. Below are some 
examples.

Statistics for newly registered users::

    from django_mstats.models import ModelStats
    from django.contrib.auth.models import User
    
    class NewUsers(ModelStats):
        model = User
        datetime_field = "date_joined"

Specifying a name::

    class NewUsers(ModelStats):
        model = User
        datetime_field = "date_joined"
        name = "User registrations"


Author
======

Django-MStats is developed by `Jonatan Heyman <http://heyman.info>`_.


License
=======

BSD License
