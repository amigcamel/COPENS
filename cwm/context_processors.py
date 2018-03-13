# -*- coding: utf-8 -*-


from forms import SearchForm

from forms import CHOICE

import itertools
iterator = itertools.count()


def include_search_form(request):
    search_form = SearchForm()
    #    query = request.session.get('query')
    #    database = request.session.get('database')
    keys = ['search_form', 'CHOICE', 'iterator']
    values = [search_form, CHOICE, iterator]
    context = dict(zip(keys, values))
    return context
