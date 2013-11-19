# -*- coding: utf-8 -*-
from django.contrib import admin
import models

class CommentInline(admin.TabularInline): 
    list_display = ('user', 'content', 'date')
    model = models.NewsComment
    extra = 2

class ArticleAdmin(admin.ModelAdmin):
    inlines = [ CommentInline]
    list_display = ('slug', 'title', 'title_en', 'date')
    search_fields = ('title', 'content')

admin.site.register(models.Article, ArticleAdmin)