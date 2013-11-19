# -*- coding: utf-8 -*-

from django.core.context_processors import csrf
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from feedback.forms import FeedbackForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import config
from livesettings import config_value
from django.conf import settings

from pages.models import Page
from news.models import Article, NewsComment
from jury.models import Jury
from partners.models import Partner
from seminars.models import Seminar, SeminarComment
from projects.forms import ParticipateForm, ProjectForm
from projects.models import Project, Nomination, ProjectComment
from users.forms import ExpertForm, ParticipantForm, ProfileForm
from users.models import Participant, Expert

PAGINATION_COUNT = 5

def get_common_context(request):
    c = {}
    c['lang'] = request.LANGUAGE_CODE
    c['request_url'] = request.path
    c['is_debug'] = settings.DEBUG
    c['recent_news'] = Article.get_list(c['lang'])[:2]
    c['recent_projects'] = Project.objects.all()[:3]
    c['recent_comments'] = ProjectComment.objects.all()[:3]
    c['ime_expert'] = Expert.exist(request.user)
    c['ime_participant'] = Participant.exist(request.user)
    c['auth'] = request.user.is_authenticated()
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
    c['home_content'] = Page.get('home', c['lang'])['content']
    c['home_about'] = Page.get('home_about', c['lang'])['content']
    c['home_projects'] = Page.get('home_projects', c['lang'])['content']
    c['home_probation'] = Page.get('home_probation', c['lang'])['content']
    return render_to_response('home.html', c, context_instance=RequestContext(request))

def about(request):
    c = get_common_context(request)
    c['p'] = Page.get('about', c['lang'])
    return render_to_response('about.html', c, context_instance=RequestContext(request))

def participate(request):
    c = get_common_context(request)
    if not c['auth']:
        return HttpResponseRedirect('/accounts/register/')
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
                                             })
            c['project_form'] = ProjectForm()
    else:
        form = ParticipateForm(request.POST, request.FILES)
        project_form = ProjectForm(request.POST)
        if form.is_valid() and project_form.is_valid():
            user.first_name = form.data['name']
            user.last_name = form.data['last_name']
            user.save()
            if 'photo' in request.FILES:
                profile.photo = request.FILES.get('photo', '')
            profile.sex = form.data.get('sex', '')
            profile.date_birth = form.data['date_birth']
            profile.school = form.data['school']
            profile.save()
            part = Participant(user=user,
                               about=form.data['about'])
            part.save()
            
            pf = project_form.save(commit=False)
            pf.participant = part
            pf.save()
            
            return HttpResponseRedirect('/project/')
        else:
            pass
        
        c['form'] = form
        c['project_form'] = project_form
    c['user_photo'] = profile.photo
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
    c['list'] = Project.get_list(c['lang'])
    return render_to_response('projects.html', c, context_instance=RequestContext(request))

def projects_nomination(request, slug):
    c = get_common_context(request)
    c['list'] = Project.get_list_nomination(c['lang'], slug)
    return render_to_response('projects.html', c, context_instance=RequestContext(request))

def project(request, slug):
    c = get_common_context(request)
    proj = Project.get(slug, c['lang'])
    c['proj'] = proj
    c['its_mine'] = proj['participant'].user == request.user
    if request.method == 'POST':
        if request.POST.get('action') == 'review':
            Project.objects.get(slug=slug).add_review(Expert.objects.get(user=request.user), 
                            request.POST.get('content'))
            return HttpResponseRedirect('/project/%s/' % slug)
        elif request.POST.get('action') == 'comment':
            Project.objects.get(slug=slug).add_comment(request.user, 
                            request.POST.get('content'))
            return HttpResponseRedirect('/project/%s/' % slug)
    return render_to_response('project.html', c, context_instance=RequestContext(request))

def news(request):
    c = get_common_context(request)
    c['list'] = Article.get_list(c['lang'])
    return render_to_response('news.html', c, context_instance=RequestContext(request))

def news_article(request, slug):
    c = get_common_context(request)
    article = Article.get(slug, c['lang'])
    c['article'] = article
    if request.method == 'POST':
        if request.POST.get('action') == 'comment':
            Article.objects.get(slug=slug).add_comment(request.user, 
                            request.POST.get('content'))
            return HttpResponseRedirect('/news/%s/' % slug)
    return render_to_response('news_item.html', c, context_instance=RequestContext(request))

def comments(request):
    c = get_common_context(request)
    c['project_comments'] = ProjectComment.objects.all()[:3]
    c['seminar_comments'] = SeminarComment.objects.all()[:3]
    c['news_comments'] = NewsComment.objects.all()[:3]
    return render_to_response('comments.html', c, context_instance=RequestContext(request))

def search(request):
    c = get_common_context(request)
    if request.method == 'POST':
        q = request.POST.get('q', '')
        if q:
            c['q'] = q
            c['projects'] = Project.search(q, c['lang'])
            c['news'] = Article.search(q, c['lang'])
            c['seminars'] = Seminar.search(q, c['lang'])
            return render_to_response('search.html', c, context_instance=RequestContext(request))
    return HttpResponseRedirect('/')

def user(request, username):
    c = get_common_context(request)
    c['user'] = User.objects.get(username=username)
    c['profile'] = c['user'].get_profile()
    c['role'] = u'Пользователь'
    if Expert.exist(c['user']):
        c['role'] = u'Эксперт'
        c['expert'] = Expert.objects.get(user=c['user']).get_(c['lang'])
    elif Participant.exist(c['user']):
        c['role'] = u'Участник'
        c['participant'] = Participant.objects.get(user=c['user'])
        
    return render_to_response('user.html', c, context_instance=RequestContext(request))

def profile(request):
    c = get_common_context(request)
    user = request.user
    participant_form = None
    expert_form = None
    profile = user.get_profile()
    profile_form = None
    
    if request.method == 'GET':
        if Participant.exist(user):
            participant = Participant.objects.get(user=user)
            participant_form = ParticipantForm(instance=participant)
        elif Expert.exist(user):
            expert = Expert.objects.get(user=user)
            expert_form = ExpertForm(instance=expert)
        profile_form = ProfileForm(instance=profile, initial={'name': user.first_name,
                                                          'last_name': user.last_name})
    else:
        if Expert.exist(user):
            expert = Expert.objects.get(user=user)
            expert_form = ExpertForm(request.POST, request.FILES)
        else:
            if Participant.exist(user):
                participant = Participant.objects.get(user=user)
                participant_form = ParticipantForm(request.POST, request.FILES)
                if participant_form.is_valid():
                    participant.about = participant_form.data['about']
                    participant.save()
            
            profile_form = ProfileForm(request.POST, request.FILES)
            if profile_form.is_valid():
                user.first_name = profile_form.data['name']
                user.last_name = profile_form.data['last_name']
                user.save()
                if 'photo' in request.FILES:
                    profile.photo = request.FILES.get('photo', '')
                profile.sex = profile_form.data.get('sex', '')
                profile.date_birth = profile_form.data['date_birth']
                profile.school = profile_form.data['school']
                profile.save()
    
    c['participant_form'] = participant_form
    c['expert_form'] = expert_form
    c['profile_form'] = profile_form
    c['user_photo'] = profile.photo
    return render_to_response('profile.html', c, context_instance=RequestContext(request))

def jury(request):
    c = get_common_context(request)
    c['list'] = Jury.get_list(c['lang'])
    return render_to_response('jury.html', c, context_instance=RequestContext(request))

def seminars(request):
    c = get_common_context(request)
    c['list'] = Seminar.get_list(c['lang'])
    return render_to_response('seminars.html', c, context_instance=RequestContext(request))

def seminar(request, slug):
    c = get_common_context(request)
    seminar = Seminar.get(slug, c['lang'])
    c['seminar'] = seminar
    if request.method == 'POST':
        if request.POST.get('action') == 'comment':
            Seminar.objects.get(slug=slug).add_comment(request.user, 
                            request.POST.get('content'))
            return HttpResponseRedirect('/seminar/%s/' % slug)
    return render_to_response('seminar.html', c, context_instance=RequestContext(request))

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
