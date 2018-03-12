from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from cwm.views import *
from brat.views import *
from control_panel.views import profile, getToken
from wordlist.views import wordlist, download_wordlist
from copenAuth import copenLogin
from about.views import *


from django.contrib import admin
admin.autodiscover()


from registration_custom.backends.default.views import RegistrationView
from cwm.forms import LopeRegForm
from django.contrib.auth.views import password_reset

urlpatterns = patterns('',
    url('^$', TemplateView.as_view(template_name='home.html'), name="home"),

    url('^profile/$', profile, name='profile'),
    url('^get_token/$', getToken, name='getToken'),

    url('^cql_tutorial/$', TemplateView.as_view(template_name='cql_tutorial.html'), name='cql_tutorial'),
    url('^search/$', search, name='search'),
    url('^download_conc$', download_conc, name='download_conc'),
    url('^download_wordlist/(.+)/$', download_wordlist, name='download_wordlist'),
    url('^concordance/(\w+)/$', 'cwm.views.con_align'),
    url('^contact/$', contact, name='contact'),
    url('^con_source/([-.:_a-zA-Z0-9]{32})/$', 'cwm.views.con_source'), 
    url('^concordance/(\w+)/$', 'cwm.views.con_align'),
    url('^concordance$', concordance, name='concordance'),
    url('^sketch$', sketch, name='sketch'),
    url('^wordlist$', wordlist, name='wordlist'),
    url('^collocation$', collocation, name='collocation'),
    url('^keyness$', keyness, name='keyness'),
    url('^emotion$', emotion, name='emotion'),
    url('^thesaurus/$', thesaurus, name='thesaurus'), 
    url('^brat/$', brat, name='brat'),
    url('^brat/(\w+)/(\w+)/$', getBrat, name="getBrat"),
    url('^setchecked/(\w+)/$', setchecked, name='setchecked'),
    url('^toc/$', TemplateView.as_view(template_name='toc.html'), name="toc"),
    url('^about_copens/$', TemplateView.as_view(template_name="about_copens.html"), name="about_copens"),
    url('^api/$', TemplateView.as_view(template_name='api.html'), name="api"),
    url('^api/', include('api.urls')),
#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^facebook/', include('django_facebook.urls')),
    url(r'^accounts/login/$', copenLogin.copenLogin, name='copenLogin'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': 'home'}),
    url(r'^accounts/register/$', RegistrationView.as_view(form_class=LopeRegForm), name='registration_register'),

#    url(r'^accounts/', include('registration_custom.auth_urls')),
    url(r'^accounts/', include('registration_custom.backends.default.urls')),

    url(r'^captcha/', include('captcha.urls')),
)

# The following patterns are for password reset
urlpatterns += patterns('django.contrib.auth.views',
    url(r'^password/change/$', 'password_change', name="password_change"),
    url(r'^password/change/done/$', 'password_change_done', name="password_change_done"),
    url(r'^password/reset/$', 'password_reset', name="password_reset"),
    url(r'^password/reset/done/$', 'password_reset_done', name='password_reset_done'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        'password_reset_confirm', name="password_reset_confirm"),
    url(r'^password/done/$', 'password_reset_complete', name="password_reset_complete")
)

