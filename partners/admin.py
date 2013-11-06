# -*- coding: utf-8 -*-
from django.contrib import admin
import models

class PartnerAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'name_en')
    search_fields = ('content', 'content_en')

admin.site.register(models.Partner, PartnerAdmin)