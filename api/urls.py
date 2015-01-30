from django.conf.urls import url, include
from api import views

urlpatterns = [
    url(r'^test/$', 'api.views.test', name='api_test'),
    url(r'^concordance/(\w+)$', 'api.views.concordance', name='api_concorance'),
    url(r'^keyness/(.+)/(\w+)/$','api.views.keyness', name='api_keyness'),
    url(r'^thesaurus/(\w+)/$','api.views.thesaurus', name='api_thesaurus'),
    url(r'^sketch/(.+)/$', 'api.views.sketch', name='api_sketch'),

#    url(r'seg/$', 'ptt.views.seg', name='seg'),
] 
