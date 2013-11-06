# -*- coding: utf-8 -*-
from django.contrib import admin
import models

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'title_en')
    search_fields = ('title', 'content')

admin.site.register(models.Article, ArticleAdmin)