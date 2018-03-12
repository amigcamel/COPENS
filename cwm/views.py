#-*-coding:utf-8-*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext
from django.core.urlresolvers import reverse

from cwm.forms import SearchForm, dbdic, ConcForm, SketchForm, KeynessForm, ColloForm

from ajilock.lock import Cypher
from CWB.CL import Corpus
cy = Cypher()

from copensTools import getKeyness, getThesaurus, getSketch, getCollocation

def con_source(request, qpos):
    window_size = 100
    corp_name, start, end = cy.decrypt(qpos)
    start, end = int(start), int(end)
    corpus = Corpus(corp_name.upper(), registry_dir='/usr/local/share/cwb/registry')
    words = corpus.attribute('word', 'p')
    corp_len = len(words)
    if start-window_size < 0:
        lb = 0
    else:
        lb = start-window_size
    if end+window_size > corp_len:
        rb = corp_len-1
    else:
        rb = end+window_size

    lw = ''.join(words[lb:start])
    qw = '<span style="color:red;font-size:24px;">'+''.join(words[start:end])+'</span>'
    rw = ''.join(words[end:rb])
    if corp_name == 'tccm' or corp_name == 'ntuspk':
        if corp_name == 'tccm':
            s_attrs = corpus.attribute('s_addresser', 's')
        if corp_name == 'ntuspk':
            s_attrs = corpus.attribute('s_speaker', 's')
        top = s_attrs.cpos2struc(lb)
        top = s_attrs[top]
        bottom = s_attrs.cpos2struc(rb)
        bottom = s_attrs[bottom]

        attr_con = []
        for attr in s_attrs:
            if attr[0] >= top[0] and attr[1] <= bottom[1]:
                attr_con.append(attr)
        output = ''
        for a in attr_con:
            if start in xrange(a[0], a[1]):
                sent =\
                a[-1] + ': ' +\
                ' '.join(words[a[0]:start]) + ' ' +\
                '<span style="color:red;font-size:24px;">' + ' '.join(words[start:end]) + '</span>' + ' ' +\
                ' '.join(words[end:a[1]])
            else:
                sent = '%s: %s' % (a[-1], ' '.join(words[a[0]:a[1]]))
            output += sent + '<br>'
                
#        output = ['%s: %s' % (i[-1], ' '.join(words[i[0]:i[1]])) for i in attr_con]
#        output = '<br>'.join(output)
        return HttpResponse(output)

    return HttpResponse(lw+qw+rw)

def make_context(request):
    query = request.session.get('query')
    database = request.session.get('database')
    context = {'query':query, 'database':database}
    return context

def search(request):
    for k in ['query', 'database', 'conclst', 'context']:
        if k in request.session.keys():
            del request.session[k]
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            database = form.cleaned_data['database']
            database = [(i, dbdic[i]) for i in database]
            request.session['query'] = query
            request.session['database'] = database
            context = make_context(request)
            return render_to_response('search.html', context, context_instance=RequestContext(request)) 
    else:
        form = SearchForm()
    return render_to_response('search.html', {'form':form}, context_instance=RequestContext(request))

import subprocess, json
from collections import Counter
def concordance(request, show_pos=0, rsize=0, auth=1, sampling_num=0):
    context = make_context(request)
    if 'window_size' in request.GET:
        context = make_context(request)
        concform = ConcForm(request.GET)
        if concform.is_valid():
            window_size = concform.cleaned_data['window_size']
            display_num = concform.cleaned_data['display_num']
            if concform.cleaned_data['sampling']:
                sampling_num = concform.cleaned_data['sampling_num']
            if concform.cleaned_data['pos']:
                show_pos, context['pos'] = 1, True
            query = request.session.get('query')

            if not request.user.is_authenticated():
                auth, rsize = 0, 5000-1
            corpus_names = [corp_raw for corp_raw, corp_name in request.session['database']]
            corpus_names = ' '.join(corpus_names)
#            conclst = getConcordance(corpus_names=corpus_names, 
#                                 query=query, 
#                                 window_size=window_size, 
#                                 show_pos=show_pos, 
#                                 rsize=rsize, 
#                                 auth=auth, 
#                                 sampling_num=sampling_num) 

            cmd = u'/home/achiii/.pyenv/versions/copens/bin/python /var/www/copens/cwm/cqpW.py -c %s -t %s -w %d -r %d -p %d -a %d -s %d' % (corpus_names, query, window_size, rsize, show_pos, auth, sampling_num)

            cmd = cmd.encode('utf8').split()
            conclst = subprocess.check_output(cmd)
            conclst = json.loads(conclst)

            request.session['conclst'] = conclst
            corp_det = Counter([item['corp_name'] for item in conclst])
            context['conclst'] = conclst
            context['corp_det'] = dict(corp_det)
            context['display_num'] = display_num
            request.session['context'] = context
    else:
        context = make_context(request)
        context['concform'] = ConcForm()
    return render_to_response('concordance.html', context, context_instance=RequestContext(request))

def con_align(request, posi):
    if request.session.get('context'):
        conclst = request.session['conclst']
        if posi == 'left':
            conclst.sort(key=lambda x:x['conc'][0][-1])
            request.session['context']['conclst'] = conclst
            return render_to_response('concordance.html', request.session['context'], context_instance=RequestContext(request))
        elif posi == 'right':
            conclst.sort(key=lambda x:x['conc'][-1][0])
            request.session['context']['conclst'] = conclst
            return render_to_response('concordance.html', request.session['context'], context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect(reverse(search))    
    else:
        return HttpResponseRedirect(reverse(search))
    

def download_conc(request):
    from django.core.servers.basehttp import FileWrapper
    import tempfile, csv

    temp = tempfile.TemporaryFile()
    conclst = request.session.get('conclst')
    if conclst:   
        if request.user.is_authenticated():
            output = [[j.encode('utf-8') for j in i['conc']] for i in conclst]
        else:
             output = [[j.encode('utf-8') for j in i['conc']] for i in conclst[:100]]
        writer = csv.writer(temp)
        writer.writerows(output)
        temp.flush()
    
        wrapper = FileWrapper(temp)
        response = HttpResponse(wrapper, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=concordance.csv'
        response['Content-Length'] = temp.tell()
        temp.seek(0)
        return response
    else:
        return HttpResponseRedirect(reverse(search))

def sketch(request):
    context = make_context(request)
    if request.method == 'POST':
        sketchform = SketchForm(request.POST)
        if sketchform.is_valid():
            query = context['query'] 
            min_logdice = sketchform.cleaned_data['min_logdice']
            min_occ = sketchform.cleaned_data['min_occ']
            context['output'] = getSketch(query, min_logdice, min_occ)
    else:
        sketchform = SketchForm()
        context['sketchform'] = sketchform
    return render_to_response('sketch.html', context, context_instance=RequestContext(request))

def keyness(request):
    context = make_context(request)
    if request.method == 'POST':
        keynessform = KeynessForm(request.POST)
        if keynessform.is_valid():
            ref_corp = keynessform.cleaned_data['reference_corpus']
            from cwm.forms import DB_CHOICE
            rescon = getKeyness(context['query'], ref_corp, context['database']) 
            context['rescon'] = rescon
    else:
#        keynessform = KeynessForm()
        context['keynessform'] = KeynessForm()
    return render_to_response('keyness.html', context, context_instance=RequestContext(request))

def thesaurus(request):
    context = make_context(request)
    word = request.session.get('query') 
    context['word_sim_list'] = getThesaurus(word)
    return render_to_response('thesaurus.html', context, context_instance=RequestContext(request))

def collocation(request):
    context = make_context(request)
    if request.method == 'POST':
        colloform = ColloForm(request.POST)
        if colloform.is_valid():
            algos = colloform.cleaned_data['algorithms']
            swf = colloform.cleaned_data['stopword_filter']
            database = request.session.get('database')
#            database = [i[0] for i in database]
            query = request.session.get('query')
            res, stopwords = getCollocation(query, database, [algos], swf)


            context['collodic'] = res
            context['stopwords'] = stopwords
    else:
        context['colloform'] = ColloForm()
    return render_to_response('collocation.html', context, context_instance=RequestContext(request))

# 尚未處理

def emotion(request):
    context = make_context(request)
    return render_to_response('emotion.html', context, context_instance=RequestContext(request))
