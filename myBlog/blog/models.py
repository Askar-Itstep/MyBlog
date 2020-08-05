from django.db import models
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse
from taggit.managers import TaggableManager

'''
Список проектов (портфолио)-возможно со ссылкой на гитхаб
Например:
Проект Спортклуб - ASP.net (клик - переход по ссылке) 
'''
class Project(models.Model):
    title = models.CharField(max_length=200,
                             db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='projects/%Y/%%m/%d',
                              blank=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title   #вывод вместо ID

    def get_absolute_url(self):
                                    #localhost/3/mywebpage
        return reverse('blog:project_detail', args=[self.id, self.slug])    #при изм. - путь при навед. мыши меняется
        # return reverse('blog:project_detail', args=[self.id])    #для работы без slug'a


###############################################################################
class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.body)