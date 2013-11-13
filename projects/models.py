# -*- coding: utf-8 -*-
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
import pytils
import config
from users.models import Participant, Expert
from django.db.models import Q

class Nomination(models.Model):
    title = models.CharField(max_length=200, verbose_name=u'заголовок рус')
    title_en = models.CharField(max_length=200, verbose_name=u'заголовок eng')
    slug = models.SlugField(max_length=100, verbose_name=u'слаг', unique=True, blank=True, help_text=u'Заполнять не нужно')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=pytils.translit.slugify(self.title)
        super(Nomination, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = u'номинация'
        verbose_name_plural = u'номинации'
        ordering=['slug']
        
    def __unicode__(self):
        return self.title
    
    @staticmethod
    def get_by_slug(slug):
        return Nomination.objects.get(slug=slug)
    
    def get_(self, lang):
        res = {'slug': self.slug }
        if lang=='en':
            res.update({'title': self.title_en })     
        else :
            res.update({'title': self.title })
        return res
    
    @staticmethod
    def get(slug, lang):
        try:
            return Nomination.objects.get(slug=slug).get_(lang)
        except:
            return None

class Project(models.Model):
    participant = models.ForeignKey(Participant, related_name='project', verbose_name=u'участник')
    nomination = models.ForeignKey(Nomination, related_name='projects', verbose_name=u'номинация')
    title = models.CharField(max_length=200, blank=True, verbose_name=u'Название')
    title_en = models.CharField(max_length=200, blank=True, verbose_name=u'Название (eng)')
    desc = models.TextField(max_length=1000, blank=True, verbose_name=u'краткое описание')
    desc_en = models.TextField(max_length=1000, blank=True, verbose_name=u'краткое описание (eng)')
    content = RichTextField(blank=True, null=True, verbose_name=u'описание')
    content_en = RichTextField(blank=True, null=True, verbose_name=u'описание (eng)')
    image = models.ImageField(upload_to= 'uploads/projects', blank=True, max_length=256, verbose_name=u'Изображение')
    file = models.FileField(upload_to= 'uploads/projects', blank=True, max_length=256, verbose_name=u'Полный файл')
    slug = models.SlugField(max_length=100, verbose_name=u'слаг', unique=True, blank=True, help_text=u'Заполнять не нужно')
    date = models.DateTimeField(verbose_name=u'дата', null=True, auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.title_en:
            self.title_en = self.title
        if not self.slug:
            self.slug=pytils.translit.slugify(self.title_en)
        super(Project, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = u'проект'
        verbose_name_plural = u'проекты'
        ordering=['-date']
        
    def __unicode__(self):
        return self.slug
    
    
    def get_(self, lang):
        res = {'image': self.image,
               'slug': self.slug,
               'file': self.file,
               'date': self.date,
               'nomination': self.nomination.get_(lang), 
               'participant': self.participant,    
               'reviews': Review.get_by_proj(self, lang),
               'comments_short': ProjectComment.get_by_proj(self)[:3],
               'comments_more': ProjectComment.get_by_proj(self)[3:],
               'comments_count': len(ProjectComment.get_by_proj(self)),
               }

        if lang=='en':
            res.update({'title': self.title_en,
                        'desc': self.desc_en,
                        'content': self.content_en})     
        else :
            res.update({'title': self.title,
                        'desc': self.desc,
                        'content': self.content})
        return res
    
    @staticmethod
    def get(slug, lang):
        try:
            return Project.objects.get(slug=slug).get_(lang)
        except:
            return None
        
    @staticmethod
    def get_list(lang):
        return [p.get_(lang) for p in Project.objects.all()]
    
    @staticmethod
    def get_list_nomination(lang, nomination):
        n = Nomination.get_by_slug(nomination)
        return [p.get_(lang) for p in Project.objects.filter(nomination=n)]
    
    @staticmethod
    def search(query, lang):
        return [p.get_(lang) for p in Project.objects.filter(Q(title__icontains=query) |
                                                             Q(title_en__icontains=query) |
                                                             Q(desc__icontains=query) |
                                                             Q(desc_en__icontains=query) |
                                                             Q(content__icontains=query) |
                                                             Q(content_en__icontains=query))]
    
    
    
    def add_review(self, expert, content):
        Review(expert=expert,
               project=self,
               content=content,
               content_en=content).save()
               
    def add_comment(self, user, content):
        ProjectComment(user=user,
               project=self,
               content=content).save()
    
class Review(models.Model):
    expert = models.ForeignKey(Expert, verbose_name=u'эксперт')
    project = models.ForeignKey(Project, related_name='reviews', verbose_name=u'проект')
    content = models.TextField(max_length=1000, verbose_name=u'содержимое ru')
    content_en = models.TextField(max_length=1000, verbose_name=u'содержимое eng')
    date = models.DateTimeField(verbose_name=u'дата', null=True, auto_now_add=True)
    
    
    class Meta:
        verbose_name = u'рецензия'
        verbose_name_plural = u'рецензии'
        ordering=['-date']
        
    def __unicode__(self):
        return u'%s к %s' % (self.expert.fio, self.project.title)
    
    def get_(self, lang):
        res = {'expert': self.expert.get_(lang) }
        if lang=='en':
            res.update({'content': self.content_en })     
        else :
            res.update({'content': self.content })
        return res
    
    @staticmethod
    def get_by_proj(proj, lang):
        return [r.get_(lang) for r in Review.objects.filter(project=proj)]
    
class ProjectComment(models.Model):
    user = models.ForeignKey(User, verbose_name=u'пользователь')
    project = models.ForeignKey(Project, related_name='comments', verbose_name=u'проект')
    content = models.TextField(max_length=1000, verbose_name=u'содержимое')
    date = models.DateTimeField(verbose_name=u'дата', null=True, auto_now_add=True)
    
    class Meta:
        verbose_name = u'комментарий'
        verbose_name_plural = u'комментарии'
        ordering=['-date']
        
    def __unicode__(self):
        return u'%s к %s' % (self.user.username, self.project.title)
    
    @staticmethod
    def get_by_proj(proj):
        return ProjectComment.objects.filter(project=proj)
