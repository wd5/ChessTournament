from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'chess_tournament.tournament.views.home_view'),
    url(r'^tournaments$', 'chess_tournament.tournament.views.tournaments_view'),
    url(r'^tournaments/(\d{1,6})$', 'chess_tournament.tournament.views.tournament_view'),
    url(r'^players$', 'chess_tournament.tournament.views.players_view'),
    # url(r'^chess_tournament/', include('chess_tournament.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
