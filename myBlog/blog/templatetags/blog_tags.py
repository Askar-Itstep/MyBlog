import markdown
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from ..models import Project

register = template.Library()


###########################################################
@register.simple_tag
def total_projects():
    return Project.objects.count()


#############################################################
@register.inclusion_tag('blog/project/latest_projects.html')
def show_latest_projects(count=3):
    latest_projects = Project.objects.order_by('-created')[:count]
    return {'latest_projects': latest_projects}

###########################################################
##-----only for Django < 1.9----
# @register.assignment_tag
# def get_most_commented_projects(count=4):
#     return Project.objects.annotate(total_projects=Count('comments')).order_by('-total_comments')[:count]

@register.simple_tag
def get_most_commented_projects(count=4):
    list = Project.objects.annotate(total_projects=Count('comments')).order_by('-comments')[:count]
    return list



################################################################
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))