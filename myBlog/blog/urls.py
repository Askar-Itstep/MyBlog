from django.contrib import admin
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.project_list, name = 'project_list'), #возващение пути (из-за тегирования)
    # path('', views.ProjectListView.as_view(), name='project_list'),

    path(r'^tag/(?P<tag_slug>[-\w]+)/$', views.project_list, name='project_list_by_tag'),

    path('<project_id>/share', views.post_share, name='post_share'),
    path(
        '<int:id>/<slug:slug>', views.project_detail, name='project_detail')
]
