# -*- coding: utf-8 -*-
from django.contrib import admin
import models

class SeminarAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'title_en')

admin.site.register(models.Seminar, SeminarAdmin)