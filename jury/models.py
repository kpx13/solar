# -*- coding: utf-8 -*-
from django.db import models
from pytils import translit

class Jury(models.Model):
    fio = models.CharField(max_length=256, verbose_name=u'ФИО ru')
    fio_en = models.CharField(max_length=256, verbose_name=u'ФИО eng')
    position = models.CharField(max_length=256, verbose_name=u'должность ru')
    position_en = models.CharField(max_length=256, verbose_name=u'должность eng')
    description = models.TextField(verbose_name=u'Описание ru')
    description_en = models.TextField(verbose_name=u'Описание eng')
    photo = models.ImageField(upload_to=lambda instance, filename: 'uploads/jury/' + translit.translify(filename),
                              default='uploads/empty_photo.jpg', blank=True, max_length=256, verbose_name=u'фото')
    
    class Meta:
        verbose_name = u'жюри'
        verbose_name_plural = u'жюри'
        ordering=['id']
        
    def __unicode__(self):
        return self.fio
    
        
    def get_(self, lang):
        res = {'photo': self.photo }
        if lang=='en':
            res.update({'fio': self.fio_en,
                        'position': self.position_en,
                        'description': self.description_en })     
        else :
            res.update({'fio': self.fio,
                        'position': self.position,
                        'description': self.description })
        return res
    
    @staticmethod
    def get(slug, lang):
        try:
            return Jury.objects.get(slug=slug).get_(lang)
        except:
            return None
        
    @staticmethod
    def get_list(lang):
        return [p.get_(lang) for p in Jury.objects.all()]
    
