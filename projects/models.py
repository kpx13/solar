# -*- coding: utf-8 -*-
from django.db import models
from ckeditor.fields import RichTextField
import pytils
import config
from users.models import Participant, Expert

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
    title = models.CharField(max_length=200, verbose_name=u'заголовок рус')
    title_en = models.CharField(max_length=200, verbose_name=u'заголовок eng')
    desc = models.TextField(max_length=1000, blank=True, verbose_name=u'краткое описание рус')
    desc_en = models.TextField(max_length=1000, blank=True, verbose_name=u'краткое описание eng')
    content = RichTextField(blank=True, verbose_name=u'контент рус')
    content_en = RichTextField(blank=True, verbose_name=u'контент eng')
    image = models.ImageField(upload_to= 'uploads/projects', blank=True, max_length=256, verbose_name=u'картинка')
    file = models.FileField(upload_to= 'uploads/projects', blank=True, max_length=256, verbose_name=u'файл с проектом')
    slug = models.SlugField(max_length=100, verbose_name=u'слаг', unique=True, blank=True, help_text=u'Заполнять не нужно')
    date = models.DateField(verbose_name=u'дата', auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.title_en:
            self.title_en = self.title
        if not self.slug:
            self.slug=pytils.translit.slugify(self.title_en)
        super(Project, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = u'проект'
        verbose_name_plural = u'проекты'
        ordering=['slug']
        
    def __unicode__(self):
        return self.slug
    
    
    def get_(self, lang):
        res = {'image': self.image,
               'file': self.file,
               'date': self.date,
               'nomination': self.nomination.get_(lang), 
               'participant': self.participant,    }
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
    
class Review(models.Model):
    expert = models.ForeignKey(Expert, verbose_name=u'эксперт')
    project = models.ForeignKey(Project, related_name='reviews', verbose_name=u'проект')
    content = models.TextField(max_length=200, verbose_name=u'содержимое ru')
    content_en = models.TextField(max_length=200, verbose_name=u'содержимое eng')
    
    class Meta:
        verbose_name = u'рецензия'
        verbose_name_plural = u'рецензии'
        
    def __unicode__(self):
        return u'%s к %s' % (self.expert.fio, self.project.title)
