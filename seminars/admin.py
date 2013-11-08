# -*- coding: utf-8 -*-
from django.contrib import admin
import models

class CommentInline(admin.TabularInline): 
    list_display = ('user', 'content', 'date')
    model = models.SeminarComment
    extra = 2

class SeminarAdmin(admin.ModelAdmin):
    inlines = [ CommentInline]
    list_display = ('slug', 'title', 'title_en')

admin.site.register(models.Seminar, SeminarAdmin)