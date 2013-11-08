# -*- coding: utf-8 -*-
from django.db import models
from ckeditor.fields import RichTextField
import pytils
import config
from users.models import Expert
from django.contrib.auth.models import User

class Seminar(models.Model):
    title = models.CharField(max_length=200, verbose_name=u'заголовок рус')
    title_en = models.CharField(max_length=200, verbose_name=u'заголовок eng')
    content = models.TextField(verbose_name=u'ссылка на видео', help_text=u'На ютубе HTML код -> копируем ссылку из атрибута src внутри кавычек. Например, //www.youtube.com/embed/vynnVjZx6rg?rel=0')
    expert = models.ForeignKey(Expert, verbose_name=u'Эксперт')
    slug = models.SlugField(max_length=100, verbose_name=u'слаг', unique=True, blank=True, help_text=u'Заполнять не нужно')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=pytils.translit.slugify(self.title_en)
        super(Seminar, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = u'семинар'
        verbose_name_plural = u'семинары'
        ordering=['slug']
        
    def __unicode__(self):
        return self.slug
    
   
    def get_(self, lang):
        res = {'content': self.content,
               'expert': self.expert.get_(lang),
               'slug': self.slug,
               'comments_short': SeminarComment.get_by_seminar(self)[:3],
               'comments_more': SeminarComment.get_by_seminar(self)[3:],
               'comments_count': len(SeminarComment.get_by_seminar(self)),    }
        if lang=='en':
            res.update({'title': self.title_en})     
        else :
            res.update({'title': self.title})
        return res
    
    @staticmethod
    def get(slug, lang):
        try:
            return Seminar.objects.get(slug=slug).get_(lang)
        except:
            return None
        
    @staticmethod
    def get_list(lang):
        return [p.get_(lang) for p in Seminar.objects.all()]
    
    def add_comment(self, user, content):
        SeminarComment(user=user,
               seminar=self,
               content=content).save()
    
class SeminarComment(models.Model):
    user = models.ForeignKey(User, verbose_name=u'пользователь')
    seminar = models.ForeignKey(Seminar, related_name='comments', verbose_name=u'проект')
    content = models.TextField(max_length=1000, verbose_name=u'содержимое')
    date = models.DateTimeField(verbose_name=u'дата', null=True, auto_now_add=True)
    
    class Meta:
        verbose_name = u'комментарий'
        verbose_name_plural = u'комментарии'
        ordering=['-date']
        
    def __unicode__(self):
        return u'%s к %s' % (self.user.username, self.seminar.title)
    
    @staticmethod
    def get_by_seminar(seminar):
        return SeminarComment.objects.filter(seminar=seminar)
