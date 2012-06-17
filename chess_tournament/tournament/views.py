from chess_tournament.tournament.models import Tournament, Player
from django.shortcuts import render_to_response


def home_view(request):
    return render_to_response('index.html', locals())


def tournaments_view(request):
    tournaments = Tournament.objects.all()
    return render_to_response('tournaments.html', locals())


def tournament_view(request, id):
    tournament = Tournament.objects.get(id = id)
    return render_to_response('tournament.html', locals())


def players_view(request):
    players = Player.objects.order_by('-rank').all()
    return render_to_response('players.html', locals())


def login_success_view(request):
    return render_to_response('login-success.html', locals())
