from django.conf.urls import url
from . import views

#*************************HANDY HELPER********************************

urlpatterns = [
    url(r'^$', views.index),                # /
    url(r'^create$', views.create),         # /create
    url(r'^login$', views.login),           # /login
    url(r'^dashboard$', views.dashboard),   # /dashboard
    url(r'^destroy$', views.destroy),       # /destroy
    url(r'^jobs/new$', views.newjob),       # /jobs/new
    url(r'^jobs/create$', views.create_job),                  # /jobs/create
    url(r'^jobs/(?P<id>\d+)/edit$', views.edit_job),          # /jobs/<id>/edit
    url(r'^jobs/update', views.update_job),                   # /jobs/update
    url(r'^jobs/(?P<id>\d+)$', views.view),                    # /jobs/<id>
    url(r'^jobs/(?P<id>\d+)/destroy$', views.destroy_job),    # /jobs/<id>/destroy
    url(r'^jobs/(?P<id>\d+)/join$', views.join),               # /jobs/<id>/join
    url(r'^jobs/(?P<id>\d+)/cancel$', views.cancel),           # /jobs/<id>/cancel
]