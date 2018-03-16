# -*- coding: utf-8 -*-

from collections import Counter

import requests

from copensTools import getKeyness
from copensTools import getThesaurus
from copensTools import getSketch
from copensTools import getCollocation


from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.template import RequestContext
from django.core.urlresolvers import reverse

from cwm.forms import SearchForm
from cwm.forms import dbdic
from cwm.forms import ConcForm
from cwm.forms import SketchForm
from cwm.forms import KeynessForm
from cwm.forms import ColloForm


def con_source(request, qpos):
    qpos = qpos.strip('/')
    resp = requests.get('http://127.0.0.1:7878/con_source', {'qpos': qpos})
    assert resp.status_code == 200
    return HttpResponse(resp.text)


def make_context(request):
    query = request.session.get('query')
    database = request.session.get('database')
    context = {'query': query, 'database': database}
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
            return render_to_response(
                'search.html',
                context,
                context_instance=RequestContext(request))
    else:
        form = SearchForm()
    return render_to_response(
        'search.html', {'form': form},
        context_instance=RequestContext(request))


def concordance(request, show_pos=0, rsize=0, auth=1, sampling_num=0):
    context = make_context(request)
    if 'window_size' in request.GET:
        context = make_context(request)
        concform = ConcForm(request.GET)
        if concform.is_valid():
            window_size = concform.cleaned_data['window_size']
            display_num = concform.cleaned_data['display_num']
            # if concform.cleaned_data['sampling']:
            #     sampling_num = concform.cleaned_data['sampling_num']
            if concform.cleaned_data['pos']:
                show_pos, context['pos'] = 1, True
            query = request.session.get('query')

            # if not request.user.is_authenticated():
            #     auth, rsize = 0, 5000 - 1
            corpus_names = [
                corp_raw for corp_raw, corp_name in request.session['database']
            ]
            corpus_names = ' '.join(corpus_names)

            params = {
                'corpus_names': corpus_names,
                'token': query,
                'window_size': window_size,
                'rsize': rsize,
                'show_pos': show_pos
            }
            url = 'http://127.0.0.1:7878/cwb'
            resp = requests.get(url, params)
            assert resp.status_code == 200
            conclst = resp.json()

            request.session['conclst'] = conclst
            corp_det = Counter([item['corp_name'] for item in conclst])
            context['conclst'] = conclst
            context['corp_det'] = dict(corp_det)
            context['display_num'] = display_num
            request.session['context'] = context
    else:
        context = make_context(request)
        context['concform'] = ConcForm()
    return render_to_response(
        'concordance.html', context, context_instance=RequestContext(request))


def con_align(request, posi):
    if request.session.get('context'):
        conclst = request.session['conclst']
        if posi == 'left':
            conclst.sort(key=lambda x: x['conc'][0][-1])
            request.session['context']['conclst'] = conclst
            return render_to_response(
                'concordance.html',
                request.session['context'],
                context_instance=RequestContext(request))
        elif posi == 'right':
            conclst.sort(key=lambda x: x['conc'][-1][0])
            request.session['context']['conclst'] = conclst
            return render_to_response(
                'concordance.html',
                request.session['context'],
                context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect(reverse(search))
    else:
        return HttpResponseRedirect(reverse(search))


def download_conc(request):
    from django.core.servers.basehttp import FileWrapper
    import tempfile
    import csv

    temp = tempfile.TemporaryFile()
    conclst = request.session.get('conclst')
    if conclst:
        if request.user.is_authenticated():
            output = [[j.encode('utf-8') for j in i['conc']] for i in conclst]
        else:
            output = [[j.encode('utf-8') for j in i['conc']]
                      for i in conclst[:100]]
        writer = csv.writer(temp)
        writer.writerows(output)
        temp.flush()

        wrapper = FileWrapper(temp)
        response = HttpResponse(wrapper, content_type='text/csv')
        response[
            'Content-Disposition'] = 'attachment; filename=concordance.csv'
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
    return render_to_response(
        'sketch.html', context, context_instance=RequestContext(request))


def keyness(request):
    context = make_context(request)
    if request.method == 'POST':
        keynessform = KeynessForm(request.POST)
        if keynessform.is_valid():
            ref_corp = keynessform.cleaned_data['reference_corpus']

            rescon = getKeyness(context['query'], ref_corp,
                                context['database'])
            context['rescon'] = rescon
    else:
        #        keynessform = KeynessForm()
        context['keynessform'] = KeynessForm()
    return render_to_response(
        'keyness.html', context, context_instance=RequestContext(request))


def thesaurus(request):
    context = make_context(request)
    word = request.session.get('query')
    context['word_sim_list'] = getThesaurus(word)
    return render_to_response(
        'thesaurus.html', context, context_instance=RequestContext(request))


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
    return render_to_response(
        'collocation.html', context, context_instance=RequestContext(request))


# 尚未處理


def emotion(request):
    context = make_context(request)
    return render_to_response(
        'emotion.html', context, context_instance=RequestContext(request))
