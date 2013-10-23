# -*- coding: utf-8 -*-
from django.db import models
from ckeditor.fields import RichTextField
import pytils

class Article(models.Model):
    title = models.CharField(max_length=128, verbose_name=u'заголовок')
    image = models.ImageField(upload_to= 'uploads/news', max_length=256, verbose_name=u'фото')
    content = models.TextField(verbose_name=u'вступительный текст')
    content_more = RichTextField(blank=True, verbose_name=u'текст в подробнее')
    date = models.DateField(verbose_name=u'дата')
    slug = models.SlugField(verbose_name=u'слаг', unique=True, blank=True, help_text=u'Заполнять не нужно')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=pytils.translit.slugify(self.title)
        super(Article, self).save(*args, **kwargs)
    
    @staticmethod
    def get_by_slug(page_name):
        try:
            return Article.objects.get(slug=page_name)
        except:
            return None
    
    class Meta:
        verbose_name = u'статья'
        verbose_name_plural = u'статьи'
        ordering=['-date']
    
    def __unicode__(self):
        return self.slug