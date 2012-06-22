from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()
urlpatterns = patterns('',
    url(r'^$', 'chess_tournament.tournament.views.home_view'),
    url(r'^tournaments$', 'chess_tournament.tournament.views.tournaments_view'),
    url(r'^tournaments/(\d{1,6})$', 'chess_tournament.tournament.views.tournament_view'),
    url(r'^tournaments/(\d{1,6})/toss$', 'chess_tournament.tournament.views.tournament_toss_view'),
    url(r'^games/(\d{1,6})$', 'chess_tournament.tournament.views.game_view'),
    url(r'^games/(\d{1,6})/set-result/(1:0|0\.5:0\.5|0:1)$', 'chess_tournament.tournament.views.game_set_result_view'),
    url(r'^players$', 'chess_tournament.tournament.views.players_view'),
    url(r'^login-success$', 'chess_tournament.tournament.views.login_success_view'),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {"template_name": "login.html"}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),

    url(r'^admin/', include(admin.site.urls)),
)
