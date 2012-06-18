from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'chess_tournament.tournament.views.home_view'),
    url(r'^tournaments$', 'chess_tournament.tournament.views.tournaments_view'),
    url(r'^tournaments/(\d{1,6})$', 'chess_tournament.tournament.views.tournament_view'),
    url(r'^tournaments/(\d{1,6})/toss$', 'chess_tournament.tournament.views.tournament_toss_view'),
    url(r'^players$', 'chess_tournament.tournament.views.players_view'),
    url(r'^login-success$', 'chess_tournament.tournament.views.login_success_view'),

    url( r'^accounts/login/$', 'django.contrib.auth.views.login', { "template_name": "login.html" } ),
    url( r'^accounts/logout/$', 'django.contrib.auth.views.logout' ),

    url(r'^admin/', include(admin.site.urls)),
)
