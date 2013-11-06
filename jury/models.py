# -*- coding: utf-8 -*-
from django.db import models
from ckeditor.fields import RichTextField
import pytils
import config
from users.models import Expert

class Jury(models.Model):
    fio = models.CharField(max_length=256, verbose_name=u'ФИО')
    photo = models.ImageField(upload_to= 'uploads/jury', blank=True, max_length=256, verbose_name=u'фото')
    position = models.CharField(max_length=256, verbose_name=u'должность')
    description = models.TextField(verbose_name=u'Описание')
    
    class Meta:
        verbose_name = u'жюри'
        verbose_name_plural = u'жюри'
        ordering=['id']
        
    def __unicode__(self):
        return self.fio
    
        
    @staticmethod
    def get_list(lang):
        return Jury.objects.all()