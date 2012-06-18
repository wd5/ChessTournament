from math import log
from operator import attrgetter


def get_rival(player, game):
    return game.playing_white_player if player == game.playing_black_player else game.playing_black_player


def get_player_game_points(player, game):
    if player == game.playing_white_player and game.result == '1:0':
        return 1
    if player == game.playing_black_player and game.result == '0:1':
        return 1
    if game.result == '0.5:0.5':
        return 0.5
    return 0


def get_rounds_count(players_number, win_prizes):
    return int(log(players_number, 2)) + int(log(win_prizes - 1, 2) if win_prizes > 1 else 0)


def get_players_position_comparator(tournament, tournament_results):
    player_rivals = {}

    def get_player_rivals_result(player):
        if player not in player_rivals:
            player_rivals_results = []
            games = player.get_all_games_in_tournament(tournament)
            rivals = set([get_rival(player, game) for game in games])
            for tournament_result in tournament_results:
                for rival in rivals:
                    if tournament_result.player == rival:
                        player_rivals_results.append(tournament_result)
            player_rivals[player] = player_rivals_results

        return player_rivals[player]

    def compare_players(player1, player2):
        player1_result = None
        player2_result = None

        # compare points
        for tournament_result in tournament_results:
            if player1 == tournament_result.player:
                player1_result = tournament_result
            if player2 == tournament_result.player:
                player2_result = tournament_result

        if not player1_result or not player2_result:
            return 0

        if player1_result.points != player2_result.points:
            return player1_result.points - player2_result.points

        # compare buchholz coefficients
        player1_rivals = get_player_rivals_result(player1)
        player2_rivals = get_player_rivals_result(player2)
        if len(player1_rivals) != len(player2_rivals):
            return len(player1_rivals) - len(player2_rivals)

        for top_rivals_count in xrange(len(player1_rivals), 0, -1):
            player1_rivals_points = 0
            player2_rivals_points = 0
            for top_rival_index in xrange(top_rivals_count):
                player1_rivals_points += player1_rivals[top_rival_index].points
                player2_rivals_points += player2_rivals[top_rival_index].points
            if player1_rivals_points != player2_rivals_points:
                return player1_rivals_points - player2_rivals_points

        # compare ranks
        return player1.rank - player2.rank

    return compare_players


def sort_players(players, tournament):
    tournament_results = sorted(tournament.results, key=attrgetter('points'), reverse=True)
    return sorted(players, cmp=get_players_position_comparator(tournament_results))


def get_games_pairs(tournament):
    games = []
    auto_win_player_result = None
    point_groups = {}
    for tournament_result in tournament.results:
        if tournament_result.points not in point_groups:
            point_groups[tournament_result.points] = []
        point_groups[tournament_result.points].append(tournament_result)

    point_groups_seq = sorted(point_groups.keys(), reverse=True)
    players_position_comparator = get_players_position_comparator(tournament, tournament.results)
    for i, points in enumerate(point_groups_seq):
        point_group = point_groups[points]
        point_group.sort(cmp=players_position_comparator)
        if len(point_group) % 2 == 1:
            if i + 1 < len(point_groups_seq):
                points_in_next_groups = point_groups_seq[i + 1]
                point_groups[points_in_next_groups].insert(0, point_group.pop())
            else:
                auto_win_player_result = point_group.pop()
        half_point_group = len(point_group) / 2
        for i in xrange(half_point_group):
            games.append((point_group[i].player, point_group[i + half_point_group].player,))

    return games, auto_win_player_result
