#-*-coding:utf-8-*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext
from django.core.urlresolvers import reverse

from about.forms import ContactForm
from misc import sendmail

def contact(request):
    if request.method == 'POST':
        contactform = ContactForm(request.POST)
        if contactform.is_valid():
            formvar = dict()
            for v in ['name', 'email', 'subject', 'message']:
                formvar[v] = contactform.cleaned_data[v]
            subject = formvar['subject'] + '(sent from %s by %s)' % (formvar['email'], formvar['name'])
            sendmail.gmail(subject, formvar['message'])
            context = {'okmsg':'Thank you! Youre message has been sent successfully!'}
            context['contactform'] = ContactForm()
    else:
        contactform = ContactForm()
        context = {'contactform':contactform}
    return render_to_response('contact.html', context, context_instance=RequestContext(request))
