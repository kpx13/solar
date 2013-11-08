# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

SEX = (('m', u'Мужской'), ('f', u'Женский'))

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', verbose_name=u'пользователь')
    photo = models.ImageField(upload_to= 'uploads/users', default='uploads/empty_photo.jpg', blank=True, max_length=256, verbose_name=u'фото')
    sex = models.CharField(max_length=256, choices=SEX, blank=True, verbose_name=u'пол')
    date_birth = models.CharField(max_length=256, blank=True, null=True, verbose_name=u'дата рождения')
    school = models.CharField(max_length=256, blank=True, verbose_name=u'ВУЗ')

    class Meta:
        verbose_name = 'профиль пользователя'
        verbose_name_plural = 'профили пользователей'
    
    def __unicode__ (self):
        return str(self.user.username)
    
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class Participant(models.Model):
    user = models.ForeignKey(User, related_name='participant', verbose_name=u'пользователь') # имя и фамилия в самом юзере
    about = models.TextField(blank=True, verbose_name=u'о себе')

    class Meta:
        verbose_name = 'участник'
        verbose_name_plural = 'участники'
    
    def __unicode__ (self):
        return str(self.user.username)
    
    @staticmethod
    def exist(user):
        try:
            return len(Participant.objects.filter(user=user)) > 0
        except:
            return False
    
    @staticmethod
    def get_project(user):
        from projects.models import Project
        return Project.objects.get(participant=Participant.objects.filter(user=user))
    
class Expert(models.Model):
    user = models.ForeignKey(User, related_name='expert', verbose_name=u'пользователь') # имя и фамилия в самом юзере
    about = models.TextField(blank=True, verbose_name=u'о себе')
    fio = models.CharField(max_length=500, verbose_name=u'ФИО ru')
    fio_en = models.CharField(max_length=500, verbose_name=u'ФИО eng')
    desc = models.CharField(max_length=500, verbose_name=u'Должность ru')
    desc_en = models.CharField(max_length=500, verbose_name=u'Должность eng')

    class Meta:
        verbose_name = 'эксперт'
        verbose_name_plural = 'эксперты'
    
    def __unicode__ (self):
        return str(self.user.username)
    
    @staticmethod
    def exist(user):
        try:
            return len(Expert.objects.filter(user=user)) > 0
        except:
            return False
    
    def get_(self, lang):
        res = {'user': self.user,
               'about': self.about    }
        if lang=='en':
            res.update({'fio': self.fio_en,
                        'desc': self.desc_en, })     
        else :
            res.update({'fio': self.fio,
                        'desc': self.desc, })
        return res