# -*- coding: utf-8 -*-

from django.core.context_processors import csrf
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from feedback.forms import FeedbackForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import config
from livesettings import config_value
from django.conf import settings

from pages.models import Page
from news.models import Article
from jury.models import Jury
from partners.models import Partner
from seminars.models import Seminar
from projects.forms import ParticipateForm, ProjectForm
from projects.models import Project, Nomination
from users.models import Participant, Expert

PAGINATION_COUNT = 5

def get_common_context(request):
    c = {}
    c['request_url'] = request.path
    c['is_debug'] = settings.DEBUG
    c['news'] = Article.objects.all()[:3]
    c['lang'] = request.LANGUAGE_CODE
    c.update(csrf(request))
    return c

def page(request, page_name):
    c = get_common_context(request)
    p = Page.get(page_name, request.LANGUAGE_CODE)
    
    if p:
        c.update({'p': p})
        return render_to_response('page.html', c, context_instance=RequestContext(request))
    else:
        raise Http404()

def home(request):
    c = get_common_context(request)
    c['request_url'] = 'home'
    c['partners'] = Partner.get_list(c['lang'])
    return render_to_response('home.html', c, context_instance=RequestContext(request))

def about(request):
    c = get_common_context(request)
    c['p'] = Page.get('about', c['lang'])
    return render_to_response('about.html', c, context_instance=RequestContext(request))

"""
    name = fields.CharField(label=u'имя')
    last_name = fields.CharField(label=u'фамилия')
    photo = fields.ImageField(required=False, label=u'фото')
    sex = fields.CharField(required=False, label=u'пол')
    date_birth = fields.DateField(required=False, label=u'дата рождения')
    school = fields.CharField(label=u'ВУЗ')
    about = fields.CharField(required=False, label=u'о себе')
    nomination = fields.CharField(label=u'номинация')
    title = fields.CharField(label=u'название работы')
"""

def participate(request):
    c = get_common_context(request)
    user = request.user
    profile = user.get_profile()
    if request.method == 'GET':
        if Participant.exist(user):
            return HttpResponseRedirect('/project/%s/' % Participant.get_project(user))
        elif Expert.exist(user):
            c['form'] = None
            c['msg'] = u'Вы эксперт, поэтому не можете принимать участие.'
        else:
            c['form'] = ParticipateForm(initial={'name': user.first_name,
                                             'last_name': user.last_name,
                                             'photo': profile.photo,
                                             'sex': profile.sex,
                                             'date_birth': profile.date_birth,
                                             'school': profile.school,
                                             'nomination': 'dizajn-proektyi-ispolzovaniya-vie-v-gorodskoj-srede',
                                             })
    else:
        form = ParticipateForm(request.POST, request.FILES)
        if form.is_valid():
            print 'VALID'
            user.first_name = form.data['name']
            user.last_name = form.data['last_name']
            user.save()
            #profile.photo = request.FILES.get('photo', '')
            profile.sex = form.data['sex']
            #profile.date_birth = form.data['date_birth']
            profile.school = form.data['school']
            profile.save()
            part = Participant(user=user,
                               about=form.data['about'])
            part.save()
            proj = Project(participant=part,
                           nomination=Nomination.get_by_slug((form.data['nomination'])),
                           title=form.data['title'])
            proj.save()
            return HttpResponseRedirect('/project/')
        else:
            pass
        
        c['form'] = form
    return render_to_response('participate.html', c, context_instance=RequestContext(request))

def edit_project(request):
    c = get_common_context(request)
    user = request.user
    profile = user.get_profile()
    proj = Participant.get_project(user)
    c['slug'] = proj.slug
    if request.method == 'GET':
        c['form'] = ProjectForm(instance=proj)
    else:
        form = ProjectForm(request.POST, request.FILES, instance=proj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/project/%s/' % Participant.get_project(user))
        else:
            pass
        c['form'] = form
    return render_to_response('edit_project.html', c, context_instance=RequestContext(request))

def projects(request):
    c = get_common_context(request)
    return render_to_response('projects.html', c, context_instance=RequestContext(request))

def project(request, slug):
    c = get_common_context(request)
    proj = Project.get(slug, c['lang'])
    c['proj'] = proj
    c['its_mine'] = proj['participant'].user == request.user
    return render_to_response('project.html', c, context_instance=RequestContext(request))

def jury(request):
    c = get_common_context(request)
    c['list'] = Jury.get_list(c['lang'])
    return render_to_response('jury.html', c, context_instance=RequestContext(request))

def seminars(request):
    c = get_common_context(request)
    c['list'] = Seminar.get_list(c['lang'])
    return render_to_response('seminars.html', c, context_instance=RequestContext(request))

def partners(request):
    c = get_common_context(request)
    c['list'] = Partner.get_list(c['lang'])
    return render_to_response('partners.html', c, context_instance=RequestContext(request))

def registration(request):
    c = get_common_context(request)
    return render_to_response('registration.html', c, context_instance=RequestContext(request))

def login(request):
    c = get_common_context(request)
    return render_to_response('login.html', c, context_instance=RequestContext(request))

def contacts(request):
    c = get_common_context(request)
    c.update({'p': Page.get('contacts', c['lang'])})
    if request.method == 'GET':
        c.update({'form': FeedbackForm()})
        return render_to_response('contacts.html', c, context_instance=RequestContext(request))
    elif request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            form = FeedbackForm()
            c['feedback_ok'] = True
        c.update({'form': form})
        return render_to_response('contacts.html', c, context_instance=RequestContext(request))
