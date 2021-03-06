import datetime
from operator import attrgetter
from chess.tournament.elo_rank import get_rank_change
from django.contrib.auth.decorators import permission_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render_to_response
from chess.tournament.models import Tournament, Player, Round, Game, TournamentResult
from chess.tournament.swiss_system import get_games_pairs, get_rounds_count, get_players_position_comparator
from django.views.decorators.csrf import csrf_protect


def home_view(request):
    return render_to_response('home.html', locals())


def tournaments_view(request):
    tournaments = Tournament.objects.all()
    return render_to_response('tournaments.html', locals())


def tournament_view(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)

    tournament_results = tournament.results
    tournament_rounds = tournament.rounds
    tournament_games = tournament.get_all_games_in_tournament()
    players_position_comparator = get_players_position_comparator(tournament_results, tournament_games)
    tournament_results = sorted(tournament_results,
        key=attrgetter('player'),
        cmp=players_position_comparator,
        reverse=True)

    players_count = len(tournament_results) or len(tournament.players.all())
    max_rounds_count = get_rounds_count(players_count, tournament.winning_places) if players_count > 1 else 0

    round_number = len(tournament_rounds)
    is_last_round = round_number >= max_rounds_count

    all_games_finished = True
    for game in tournament_games:
        if game.result == 'vs':
            all_games_finished = False
            break

    tournament_finished = max_rounds_count > 0 and\
                          all_games_finished and\
                          is_last_round
    can_tournament_toss = max_rounds_count > 0 and\
                          all_games_finished and\
                          not is_last_round and\
                          request.user.has_perm('tournament.create_rounds')

    return render_to_response('tournament.html', locals())


@csrf_protect
@transaction.commit_on_success
@permission_required('tournament.create_rounds', raise_exception=True)
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
    max_rounds_count = get_rounds_count(len(tournament_players), tournament.winning_places)
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
                round.auto_win_player = auto_win_player
                round.save()
                tournament_result.points += 1
                tournament_result.save()

    return HttpResponse()


def game_view(request, tournament_id, game_id):
    game = Game.objects.get(id=game_id)
    tournament = game.round.tournament
    can_enter_result = request.user.has_perm('tournament.enter_game_results')
    return render_to_response('game.html', locals())


def _get_player_game_result(result, play_white):
    if result == '1:0' and play_white:
        return 1
    elif result == '0.5:0.5':
        return 0.5
    elif result == '0:1' and not play_white:
        return 1
    else:
        return 0


def _get_points_change(previous_result, new_result, play_white):
    change = 0.0
    change -= _get_player_game_result(previous_result, play_white)
    change += _get_player_game_result(new_result, play_white)
    return change


@csrf_protect
@transaction.commit_on_success
@permission_required('tournament.enter_game_results', raise_exception=True)
def game_set_result_view(request, tournament_id, game_id, result):
    game = Game.objects.get(id=game_id)

    # save game result
    previous_result = game.result
    playing_white_player = game.playing_white_player
    playing_black_player = game.playing_black_player

    # increase players games count
    if previous_result == 'vs':
        playing_white_player.game_count += 1
        playing_black_player.game_count += 1

    # restore players rank if correcting result
    playing_white_player.rank -= game.playing_white_player_rank_change
    playing_black_player.rank -= game.playing_black_player_rank_change

    # calculating players rank changes
    game.playing_white_player_rank_change = get_rank_change(playing_white_player.rank,
        playing_white_player.game_count,
        playing_black_player.rank,
        _get_player_game_result(result, True))
    game.playing_black_player_rank_change = get_rank_change(playing_black_player.rank,
        playing_black_player.game_count,
        playing_white_player.rank,
        _get_player_game_result(result, False))

    # change players ranks
    playing_white_player.rank += game.playing_white_player_rank_change
    playing_black_player.rank += game.playing_black_player_rank_change

    # update game changes
    game.result = result
    game.save()

    # update players rank changes
    playing_white_player.save()
    playing_black_player.save()

    # update tournament result
    for tournament_result in game.round.tournament.results:
        if game.playing_white_player == tournament_result.player:
            tournament_result.points += _get_points_change(previous_result, result, True)
            tournament_result.save()
        if game.playing_black_player == tournament_result.player:
            tournament_result.points += _get_points_change(previous_result, result, False)
            tournament_result.save()

    return HttpResponse()


def players_view(request):
    players = Player.objects.order_by('-rank').all()
    return render_to_response('players.html', locals())


def login_success_view(request):
    return render_to_response('login-success.html', locals())
