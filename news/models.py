# -*- coding: utf-8 -*-
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db.models import Q
from pytils import translit
import pytils

class Article(models.Model):
    title = models.CharField(max_length=128, verbose_name=u'заголовок ru')
    title_en = models.CharField(max_length=128, verbose_name=u'заголовок eng')
    image = models.ImageField(upload_to=lambda instance, filename: 'uploads/news/' + translit.translify(filename),
                              default='uploads/empty_photo.jpg', blank=True, max_length=256, verbose_name=u'картинка')
    content = models.TextField(verbose_name=u'краткое описание ru')
    content_more = RichTextField(blank=True, verbose_name=u'текст в подробнее ru')
    content_en = models.TextField(verbose_name=u'краткое описание eng')
    content_more_en = RichTextField(blank=True, verbose_name=u'текст в подробнее eng')
    date = models.DateTimeField(verbose_name=u'дата', auto_now_add=True)
    slug = models.SlugField(verbose_name=u'слаг', unique=True, blank=True, help_text=u'Заполнять не нужно')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=pytils.translit.slugify(self.title)
        super(Article, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = u'новость'
        verbose_name_plural = u'новости'
        ordering=['-date']
    
    def __unicode__(self):
        return self.slug
    
    
    def get_(self, lang):
        res = {'image': self.image,
               'date': self.date,
               'slug': self.slug,
               'comments_short': NewsComment.get_by_article(self)[:3],
               'comments_more': NewsComment.get_by_article(self)[3:],
               'comments_count': len(NewsComment.get_by_article(self)),    }
        if lang=='en':
            res.update({'title': self.title_en,
                        'content': self.content_en,
                        'content_more': self.content_more_en})     
        else :
            res.update({'title': self.title,
                        'content': self.content,
                        'content_more': self.content_more })
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
    
    @staticmethod
    def search(query, lang):
        return [p.get_(lang) for p in Article.objects.filter(Q(title__icontains=query) |
                                                             Q(title_en__icontains=query) |
                                                             Q(content_more__icontains=query) |
                                                             Q(content_more_en__icontains=query) |
                                                             Q(content__icontains=query) |
                                                             Q(content_en__icontains=query))]
    
    def add_comment(self, user, content):
        NewsComment(user=user,
               article=self,
               content=content).save()
    
class NewsComment(models.Model):
    user = models.ForeignKey(User, verbose_name=u'пользователь')
    article = models.ForeignKey(Article, related_name='comments', verbose_name=u'статья')
    content = models.TextField(max_length=1000, verbose_name=u'содержимое')
    date = models.DateTimeField(verbose_name=u'дата', null=True, auto_now_add=True)
    
    class Meta:
        verbose_name = u'комментарий'
        verbose_name_plural = u'комментарии'
        ordering=['-date']
        
    def __unicode__(self):
        return u'%s к %s' % (self.user.username, self.article.title)
    
    @staticmethod
    def get_by_article(article):
        return NewsComment.objects.filter(article=article)

    