import os
import environ
# import environ
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from taggit.models import Tag

from .forms import CommentForm, EmailPostForm
from .models import Project


# -отображ. списка проектов 1)-------
# def project_list(request, project_slug = None):
#     projects = Project.objects.all()
#     if project_slug:
#         projects = projects.filter(slug=project_slug)
#     paginator = Paginator(projects, per_page=2)
#     page = request.GET.get('page')
#     try:
#         projects = paginator.page(page)
#     except PageNotAnInteger:
#         projects = paginator.page(1)
#     except EmptyPage:
#         projects = paginator.page(paginator.num_pages)
#     return render(request,
#                   'blog/project/list.html', # -path directory
#                   {'projects':projects, 'page':page} )

##--2)---------------------
# class ProjectListView(ListView):
#     queryset = Project.objects.all()
#     context_object_name = 'projects'
#     paginate_by = 2
#     template_name = 'blog/project/list.html'

##--3)-----------------------
def project_list(request, project_slug = None, tag_slug=None):
    object_list = Project.objects.all()
    tag = None
    # env = environ.Env(
    #     DEBUG=(bool, False)
    # )
    # print('.env:', env.str('EMAIL_HOST_USER'))
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 2)
    page = request.GET.get('page')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        projects = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        projects = paginator.page(paginator.num_pages)
    return render(request, 'blog/project/list.html', {'page': page,
                                                      'projects': projects,
                                                      'tag': tag})


# ===============отображ. проекта в деталях==================

def project_detail(request, id, slug):
    project = get_object_or_404(Project, id=id, slug=slug)
    comments = project.comments.filter(active=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current project to the comment
            new_comment.project = project
            # Save the comment to the database
            new_comment.save()
        # else:
        # print(comment_form.errors)
    else:
        comment_form = CommentForm()
                        ## Получение записей по сходству
    project_tags_ids = project.tags.values_list('id', flat=True)
    similar_project = Project.objects.all().filter(tags__in=project_tags_ids).exclude(id=project.id)
    similar_project = similar_project.annotate(same_tags=Count('tags')).order_by('-same_tags')[:4]
    return render(request,
                  'blog/project/detail.html',
                  {'project': project,
                   'comments': comments,
                   'comment_form': comment_form,
                    'similar_project': similar_project})


# def project_detail(request, id, slug):  #, slug - можно удалить
#     project = get_object_or_404(Project, id=id, slug=slug)
#     return render(request, 'blog/project/detail.html',
#                   context={'project':project})


##--------------------------EMAIL------------------
# def post_share(request, project_id):
#     project = get_object_or_404(Project, id=project_id)
#     if request.method == 'POST':
#         form = EmailPostForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#     else:
#         form = EmailPostForm()
#     return render(request, 'blog/project/share.html', {'project': project,
#                                                     'form': form})

# -теперь не использ.-ся?
def post_share(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            project_url = request.build_absolute_uri(project.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"' \
                .format(cd['name'], cd['email'], project.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}' \
                .format(project.title, project_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'itstep.karaganda0@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()  # my form (form.py)
    return render(request, 'blog/project/share.html', {'project': project,
                                                       'form': form,
                                                       'sent': sent})
