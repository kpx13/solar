# -*- coding: utf-8 -*-
from django.db import models
from ckeditor.fields import RichTextField
import pytils

class Article(models.Model):
    title = models.CharField(max_length=128, verbose_name=u'заголовок ru')
    title_en = models.CharField(max_length=128, verbose_name=u'заголовок eng')
    image = models.ImageField(upload_to= 'uploads/news', blank=True, max_length=256, verbose_name=u'картинка')
    content = models.TextField(verbose_name=u'вступительный текст ru')
    content_more = RichTextField(blank=True, verbose_name=u'текст в подробнее ru')
    content_en = models.TextField(verbose_name=u'вступительный текст eng')
    content_more_en = RichTextField(blank=True, verbose_name=u'текст в подробнее eng')
    date = models.DateTimeField(verbose_name=u'дата', auto_now_add=True)
    slug = models.SlugField(verbose_name=u'слаг', unique=True, blank=True, help_text=u'Заполнять не нужно')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=pytils.translit.slugify(self.title)
        super(Article, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = u'статья'
        verbose_name_plural = u'статьи'
        ordering=['-date']
    
    def __unicode__(self):
        return self.slug
    
    
    def get_(self, lang):
        res = {'image': self.image,
               'date': self.date    }
        if lang=='en':
            res.update({'title': self.title_en,
                        'content': self.content_en,
                        'content_more': self.content_more_en})     
        else :
            res.update({'name': self.name,
                        'content': self.content})
        return res
    
    @staticmethod
    def get(slug, lang):
        try:
            return Article.objects.get(slug=slug).get_(lang)
        except:
            return None
        
    @staticmethod
    def get_list(lang):
        return [p.get_(lang) for p in Article.objects.all()]
    
    
    