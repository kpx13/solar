# -*- coding: utf-8 -*-
from django.db import models
from ckeditor.fields import RichTextField
import pytils
import config

class Partner(models.Model):
    name = models.CharField(max_length=200, verbose_name=u'название рус')
    name_en = models.CharField(max_length=200, verbose_name=u'название eng')
    content = models.TextField(blank=True, verbose_name=u'контент рус')
    content_en = models.TextField(blank=True, verbose_name=u'контент eng')
    url = models.CharField(max_length=200, blank=True, verbose_name=u'url сайта')
    logo = models.ImageField(upload_to= 'uploads/partners', blank=True, max_length=256, verbose_name=u'лого')
    slug = models.SlugField(max_length=100, verbose_name=u'слаг', unique=True, blank=True, help_text=u'Заполнять не нужно')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=pytils.translit.slugify(self.name_en)
        super(Partner, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = u'партнер'
        verbose_name_plural = u'партнеры'
        ordering=['slug']
        
    def __unicode__(self):
        return self.slug
    
    
    def get_(self, lang):
        res = {'url': self.url,
               'logo': self.logo, }
        if lang=='en':
            res.update({'name': self.name_en,
                        'content': self.content_en})     
        else :
            res.update({'name': self.name,
                        'content': self.content})
        return res
    
    @staticmethod
    def get(slug, lang):
        try:
            return Partner.objects.get(slug=slug).get_(lang)
        except:
            return None
        
    @staticmethod
    def get_list(lang):
        return [p.get_(lang) for p in Partner.objects.all()]
    