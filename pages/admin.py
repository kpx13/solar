# -*- coding: utf-8 -*-
from django.contrib import admin
import models

class PageAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'title_en')
    search_fields = ('title', 'title_en', 'content', 'content_en')

admin.site.register(models.Page, PageAdmin)