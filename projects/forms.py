# -*- coding: utf-8 -*-
 
from django.forms import ModelForm, Form, fields
from models import Project
 
class ParticipateForm(Form):
    name = fields.CharField(label=u'имя')
    last_name = fields.CharField(label=u'фамилия')
    photo = fields.ImageField(required=False, label=u'фото')
    sex = fields.CharField(required=False, label=u'пол')
    date_birth = fields.DateField(required=False, label=u'дата рождения')
    school = fields.CharField(label=u'ВУЗ')
    about = fields.CharField(required=False, label=u'о себе')

class ProjectForm(ModelForm):
    
    class Meta:
        model = Project
        exclude = ('participant', 'slug', 'date', 'show')
    
"""
class RegisterOptForm(ModelForm):
    
    class Meta:
        model = UserProfile
        exclude = ('user', )
    
    fio = fields.CharField(label=u'ФИО')
    email = fields.EmailField(label=u'email')
    password_1 = fields.CharField(label=u'пароль 1', widget=PasswordInput)
    password_2 = fields.CharField(label=u'пароль 2', widget=PasswordInput)
    phone = fields.CharField(label=u'телефон')
    city = fields.CharField(label=u'город')
    organization = fields.CharField(label=u'организация')
    address = fields.CharField(label=u'адрес')
"""