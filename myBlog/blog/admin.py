from django.contrib import admin

# Register your models here.
from .models import Project, Comment


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_filter = ['title', 'description','created', 'update']
    list_editable = ['image', 'description']
    list_display = ['title', 'slug', 'image','description','created', 'update']
    prepopulated_fields = {'slug': ('title',) } #автозаполнение


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'email', 'project', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
    list_editable = ('body', 'email', 'project')
