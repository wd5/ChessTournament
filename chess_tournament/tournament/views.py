import datetime
from operator import attrgetter
from django.db import transaction
from django.shortcuts import render_to_response
from chess_tournament.tournament.models import Tournament, Player, Round, Game, TournamentResult
from chess_tournament.tournament.swiss_system import get_games_pairs, get_rounds_count, get_players_position_comparator


def home_view(request):
    return render_to_response('index.html', locals())


def tournaments_view(request):
    tournaments = Tournament.objects.all()
    return render_to_response('tournaments.html', locals())


def tournament_view(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)

    tournament_results = tournament.results
    tournament_games = tournament.get_all_games_in_tournament()
    players_position_comparator = get_players_position_comparator(tournament_results, tournament_games)
    tournament_results = sorted(tournament_results,
        key=attrgetter('player'),
        cmp=players_position_comparator,
        reverse=True)

    max_rounds_count = get_rounds_count(len(tournament.players.all()), tournament.win_prizes_count)
    round_number = len(tournament.rounds)
    is_last_round = round_number >= max_rounds_count

    all_games_finished = True
    for game in tournament_games:
        if game.result == 'vs':
            all_games_finished = False
            break
    return render_to_response('tournament.html', locals())


@transaction.commit_on_success
def tournament_toss_view(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    tournament_players = tournament.players.all()

    # create tournament results if no created yet
    for player in tournament_players:
        not_exits = True
        for tournament_result in tournament.results:
            if player == tournament_result.player:
                not_exits = False
                break
        if not_exits:
            tournament_result = TournamentResult(tournament=tournament, player=player)
            tournament_result.save()

    # create round
    max_rounds_count = get_rounds_count(len(tournament_players), tournament.win_prizes_count)
    round_number = len(tournament.rounds) + 1
    if round_number > max_rounds_count:
        raise
    round = Round(tournament=tournament, number=round_number, start_date=datetime.date.today())
    round.save()

    # create games
    tournament_results = tournament.results
    tournament_games = tournament.get_all_games_in_tournament()
    game_pairs, auto_win_player = get_games_pairs(tournament_results, tournament_games)
    for game_pair in game_pairs:
        game = Game(round=round,
            playing_white_player=game_pair[0],
            playing_black_player=game_pair[1],
            start_date=datetime.datetime.now())
        game.save()

    # increase last player points if odd players count
    if auto_win_player:
        for tournament_result in tournament_results:
            if auto_win_player == tournament_result.player:
                tournament_result.points += 1
                tournament_result.save()

    # sort results
    players_position_comparator = get_players_position_comparator(tournament_results, tournament_games)
    tournament_results = sorted(tournament_results,
        key=attrgetter('player'),
        cmp=players_position_comparator,
        reverse=True)

    # render response
    is_last_round = round_number >= max_rounds_count
    all_games_finished = True
    for game in tournament.get_all_games_in_tournament():
        if game.result == 'vs':
            all_games_finished = False
            break
    return render_to_response('tournament.html', locals())


def game_view(request, game_id):
    game = Game.objects.get(id=game_id)
    return render_to_response('game.html', locals())


def _get_points_change(previous_result, new_result, play_white):
    change = 0.0

    if previous_result == '1:0' and play_white:
        change -= 1
    elif previous_result == '0.5:0.5':
        change -= 0.5
    elif previous_result == '0:1' and not play_white:
        change -= 1

    if new_result == '1:0' and play_white:
        change += 1
    elif new_result == '0.5:0.5':
        change += 0.5
    elif new_result == '0:1' and not play_white:
        change += 1

    return change


@transaction.commit_on_success
def game_set_result_view(request, game_id, result):
    game = Game.objects.get(id=game_id)

    # save game result
    previous_result = game.result
    game.result = result
    game.save()

    # update tournament result
    for tournament_result in game.round.tournament.results:
        if game.playing_white_player == tournament_result.player:
            tournament_result.points += _get_points_change(previous_result, result, True)
            tournament_result.save()
        if game.playing_black_player == tournament_result.player:
            tournament_result.points += _get_points_change(previous_result, result, False)
            tournament_result.save()

    return render_to_response('game.html', locals())


def players_view(request):
    players = Player.objects.order_by('-rank').all()
    return render_to_response('players.html', locals())


def login_success_view(request):
    return render_to_response('login-success.html', locals())
