# -*- coding: utf-8 -*-
from django.contrib import admin
import models

class JuryAdmin(admin.ModelAdmin):
    list_display = ('fio', 'photo', 'position')

admin.site.register(models.Jury, JuryAdmin)