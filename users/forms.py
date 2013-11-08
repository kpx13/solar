# -*- coding: utf-8 -*-
 
from django.forms import ModelForm, Form, fields
from models import UserProfile, Expert, Participant
 
class ParticipateForm(Form):
    name = fields.CharField(label=u'имя')
    last_name = fields.CharField(label=u'фамилия')
    photo = fields.ImageField(required=False, label=u'фото')
    sex = fields.CharField(required=False, label=u'пол')
    date_birth = fields.DateField(required=False, label=u'дата рождения')
    school = fields.CharField(label=u'ВУЗ')
    about = fields.CharField(required=False, label=u'о себе')
    nomination = fields.CharField(label=u'номинация')
    title = fields.CharField(label=u'название работы')

class ProfileForm(ModelForm):
    name = fields.CharField(label=u'имя')
    last_name = fields.CharField(label=u'фамилия')
    
    class Meta:
        model = UserProfile
        exclude = ('user', )

class ExpertForm(ModelForm):
    class Meta:
        model = Expert
        exclude = ('user', )
        
class ParticipantForm(ModelForm):
    class Meta:
        model = Participant
        exclude = ('user', )
    