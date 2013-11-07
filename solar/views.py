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

def participate(request):
    c = get_common_context(request)
    return render_to_response('participate.html', c, context_instance=RequestContext(request))

def projects(request):
    c = get_common_context(request)
    return render_to_response('projects.html', c, context_instance=RequestContext(request))

def project(request, slug):
    c = get_common_context(request)
    return render_to_response('project.html', c, context_instance=RequestContext(request))

def jury(request):
    c = get_common_context(request)
    c['list'] = Jury.get_list(c['lang'])
    return render_to_response('jury.html', c, context_instance=RequestContext(request))

def seminars(request):
    c = get_common_context(request)
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
