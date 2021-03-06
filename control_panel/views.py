# -*- coding: utf-8 -*-


'''ref:http://stackoverflow.com/a/14838307/1105489'''


from django.shortcuts import render_to_response

from django.http import HttpResponseRedirect

from django.template import RequestContext
from django.core.urlresolvers import reverse

# from rest_framework.authtoken.models import Token


def profile(request):
    if request.user.is_authenticated():
        return render_to_response(
            'control_panel.html', context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('home'))


def getToken(request):
    if request.user.is_authenticated():
        if 'auth_token' not in request.user.__dict__:
            # token = Token.objects.create(user=request.user)
            return HttpResponseRedirect(reverse(profile))
    return HttpResponseRedirect(request.build_absolute_uri(reverse('home')))
