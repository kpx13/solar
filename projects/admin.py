# -*- coding: utf-8 -*-
from django.contrib import admin
import models

class NominationAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_en', 'slug')

class ReviewInline(admin.TabularInline): 
    list_display = ('expert', 'content', 'date')
    model = models.Review
    extra = 1
    
class CommentInline(admin.TabularInline): 
    list_display = ('user', 'content', 'date')
    model = models.ProjectComment
    extra = 1
    
class LikeInline(admin.TabularInline): 
    list_display = ('user', 'date')
    model = models.ProjectLike
    extra = 0

class ProjectAdmin(admin.ModelAdmin):
    inlines = [ ReviewInline, CommentInline, LikeInline]
    list_display = ('slug', 'title', 'title_en', 'desc', 'date')

admin.site.register(models.Nomination, NominationAdmin)
admin.site.register(models.Project, ProjectAdmin)