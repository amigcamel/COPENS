# -*- coding: utf-8 -*-


from cwm.forms import DB_CHOICE
from cwm.copensTools import getKeyness
from cwm.copensTools import getThesaurus
from cwm.copensTools import getSketch
from django.http import HttpResponse
# from django.http import JsonResponse --> works for django > 1.7

from rest_framework.decorators import throttle_classes
from rest_framework.decorators import api_view
from rest_framework.response import Response


from rest_framework.throttling import UserRateThrottle

import json


def jsonDump(dic):
    return json.dumps(dic, ensure_ascii=False, indent=4)


@api_view(['GET'])
def test(request):
    return HttpResponse(jsonDump({'status': 'ok'}))


@api_view(['GET'])
@throttle_classes([UserRateThrottle])
def concordance(request, query):
    return Response(query)


#    if request.method == 'GET':
#        return HttpResponse(request.user)
#        return HttpResponse(json.dumps({'test':'ok'}), content_type="application/json")

#    return HttpResponse('ok')
#    res = mongoDB('PTT', board)
#    if request.method == 'GET':
#        pttcon = []
#        for r in res.find({}, {'_id':0, 'post_time':1, 'title':1, 'content':1}).limit(10):
#            tmp = Ptt(r["post_time"],r["title"],r["content"])
#            pttcon.append(tmp)
#        serializedList = PttSerializer(pttcon, many=True)
#        return Response(serializedList.data)


@api_view(['GET'])
@throttle_classes([UserRateThrottle])
def keyness(request, query, tar_corp):
    database = DB_CHOICE
    res = getKeyness(query, tar_corp, database)
    return HttpResponse(jsonDump(res), content_type="application/json")
    return HttpResponse(jsonDump(res))


@api_view(['GET'])
@throttle_classes([UserRateThrottle])
def thesaurus(request, word):
    res = getThesaurus(word)

    return HttpResponse(jsonDump(res))


@api_view(['GET'])
@throttle_classes([UserRateThrottle])
def sketch(request, query):
    res = getSketch(query)

    return HttpResponse(jsonDump(res), content_type="application/json")
    return HttpResponse(res, content_type="application/json")
