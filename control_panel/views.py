#-*-coding:utf-8-*-
'''ref:http://stackoverflow.com/a/14838307/1105489'''

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext
from django.core.urlresolvers import reverse

from rest_framework.authtoken.models import Token

def profile(request):
    if request.user.is_authenticated():
        return render_to_response('control_panel.html', context_instance=RequestContext(request))
    else: 
        return HttpResponseRedirect(reverse('home'))


def getToken(request):
    if request.user.is_authenticated():
        if not request.user.__dict__.has_key('auth_token'):
            token = Token.objects.create(user=request.user) 
            return HttpResponseRedirect(reverse(profile))
    return HttpResponseRedirect(request.build_absolute_uri(reverse('home')))
    
    
