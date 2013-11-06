# -*- coding: utf-8 -*-
from django.db import models
from ckeditor.fields import RichTextField
import pytils
import config

class Page(models.Model):
    title = models.CharField(max_length=200, verbose_name=u'заголовок рус')
    title_en = models.CharField(max_length=200, verbose_name=u'заголовок eng')
    content = RichTextField(blank=True, verbose_name=u'контент рус')
    content_en = RichTextField(blank=True, verbose_name=u'контент eng')
    header_content = models.TextField(blank=True, verbose_name=u'html-содержимое head')
    slug = models.SlugField(max_length=100, verbose_name=u'слаг', unique=True, blank=True, help_text=u'Заполнять не нужно')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=pytils.translit.slugify(self.title_en)
        super(Page, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = u'статическая страница'
        verbose_name_plural = u'статические страницы'
        ordering=['slug']
        
    def __unicode__(self):
        return self.slug
    
    @staticmethod
    def get(slug, lang):
        try:
            page = Page.objects.get(slug=slug)
            if lang=='en':
                return {'title': page.title_en,
                        'content': page.content_en,
                        'header_content': page.header_content
                        }
            else :
                return {'title': page.title,
                        'content': page.content,
                        'header_content': page.header_content
                        }
        except:
            return None