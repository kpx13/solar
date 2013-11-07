# -*- coding: utf-8 -*-
from django.contrib import admin
import models

class NominationAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_en', 'slug')

class ReviewInline(admin.TabularInline): 
    list_display = ('expert', 'content')
    model = models.Review
    extra = 2

class ProjectAdmin(admin.ModelAdmin):
    inlines = [ ReviewInline, ]
    list_display = ('slug', 'title', 'title_en', 'desc')

admin.site.register(models.Nomination, NominationAdmin)
admin.site.register(models.Project, ProjectAdmin)