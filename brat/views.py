from django.shortcuts import render
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext
from django.core.urlresolvers import reverse

from forms import *
from datetime import datetime

from brat.models import BratModel

from django.conf import settings
import os, sys

sys.path.append('/var/www/html/project/bratAdapter')
TAR_URL = 'http://140.112.147.121/brat/#/unchecked/%s/%s'

def brat(request): 
    if request.method == 'POST':
#        form = UploadFile(request.POST, request.FILES)
        form1 = UploadFile(request.POST, request.FILES)
        form2 = BratModelForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            if request.FILES:
                bratModel = form2.save(commit=False)

 
                uf = request.FILES['upload_file']
                file_name = form2.cleaned_data['file_name']
                folder_name = form2.cleaned_data['folder_name']


                file_name = '%s_%s' % (file_name, datetime.now().strftime('%Y%m%d%H%M%S%f'))
                source_file = os.path.join(settings.UPLOAD_FILE_DIRS, file_name+'.txt')

                with open(source_file, 'wb+') as f:
                    for chunk in uf.chunks():
                        f.write(chunk)
                cmd = '/usr/bin/python2.7 /var/www/html/project/bratAdapter/bratShell.py %s %s %s' % (source_file, file_name, folder_name) 
                os.system(cmd)
                target_url = TAR_URL % (folder_name, file_name)
   
                bratModel.file_name = file_name
                bratModel.user_name = request.user
                bratModel.save()

                return render_to_response('brat.html', {'target_url': target_url, 'folder_name':folder_name}, context_instance=RequestContext(request))

    else:
        form1 = UploadFile()
        form2 = BratModelForm(initial={'folder_name':request.user})
        unchk = BratModel.objects.filter(user_name=request.user).values()
        unchk = [(i['folder_name'], i['file_name']) for i in unchk]
        return render_to_response('brat.html', {'form1':form1, 'form2':form2, 'unchk':unchk}, context_instance=RequestContext(request))
    return render_to_response('brat.html', {'form1':form1, 'form2':form2}, context_instance=RequestContext(request))

def setchecked(request, folder_name):
    os.system('python /var/www/html/project/setChecked/setChecked.py /var/www/html/brat/data/unchecked/%s copener' % folder_name)
    BratModel.objects.filter(folder_name=folder_name).delete()
    return HttpResponseRedirect(reverse('brat'))

def getBrat(request, folder_name, file_name):
    target_url = TAR_URL % (folder_name, file_name) 
    return render_to_response('brat.html', {'target_url':target_url, 'folder_name':folder_name}, context_instance=RequestContext(request))
