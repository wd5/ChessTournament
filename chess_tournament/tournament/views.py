import datetime
from django.shortcuts import render_to_response
from chess_tournament.tournament.models import Tournament, Player, Round, Game
from chess_tournament.tournament.swiss_system import get_games_pairs


def home_view(request):
    return render_to_response('index.html', locals())


def tournaments_view(request):
    tournaments = Tournament.objects.all()
    return render_to_response('tournaments.html', locals())


def tournament_view(request, id):
    tournament = Tournament.objects.get(id = id)
    return render_to_response('tournament.html', locals())


def tournament_toss_view(request, id):
    tournament = Tournament.objects.get(id = id)
    round_number = len(tournament.rounds) + 1
    round = Round(tournament=tournament, number=round_number, start_date=datetime.date.today())
    round.save()
    game_pairs, auto_win_player_result = get_games_pairs(tournament)
    for game_pair in game_pairs:
        game = Game(round=round, playing_white_player=game_pair[0], playing_black_player=game_pair[1], start_date=datetime.datetime.now())
        game.save()
    if auto_win_player_result:
        auto_win_player_result.points += 1
        auto_win_player_result.save()

    return render_to_response('tournament.html', locals())


def players_view(request):
    players = Player.objects.order_by('-rank').all()
    return render_to_response('players.html', locals())


def login_success_view(request):
    return render_to_response('login-success.html', locals())
