#-*-coding:utf-8-*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import Context, RequestContext
from cwm.forms import dbdic
from wordlist.forms import WordlistForm
from cwm.copensTools import getWordlist
from django.core.urlresolvers import reverse


def wordlist(request, stopword_level=None):
    if request.method == 'POST':
        form = WordlistForm(request.POST)
        if form.is_valid():
            stopwords = form.cleaned_data['stopwords']
            if stopwords == True:
                stopword_level = form.cleaned_data['stopword_level']
            punctuations = form.cleaned_data['punctuations']
            topnword = form.cleaned_data['topnword']
            database = form.cleaned_data['database']
            database = [(i, dbdic[i]) for i in database]
            output = getWordlist(database=database, topnword=topnword, punctuations=punctuations, stopwords=stopwords, stopword_level=stopword_level)
            request.session['wordlist'] = output
            context = {'database':database, 'output':output}
            return render_to_response('wordlist.html', context, context_instance=RequestContext(request))
    else:
        form = WordlistForm()
    return render_to_response('wordlist.html', {'form':form}, context_instance=RequestContext(request))

def download_wordlist(request, corpus_name):
    from django.core.servers.basehttp import FileWrapper
    import tempfile, csv

    temp = tempfile.TemporaryFile()

    wordlist = request.session.get('wordlist')
    if wordlist:
        res = wordlist[corpus_name]
        res = [[i['tok'].encode('utf8'), i['occ'], i['freq']] for i in res]
        res.insert(0, ['word', 'occurrence', 'frequency']) 
        writer = csv.writer(temp)
        writer.writerows(res)
        temp.flush()

        wrapper = FileWrapper(temp)
        response = HttpResponse(wrapper, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % corpus_name.encode('utf8')
        response['Content-Length'] = temp.tell()
        temp.seek(0)
        return response       

    else:
        return HttpResponseRedirect(reverse(wordlist))
