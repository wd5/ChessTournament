from math import log


def get_rounds_count(players_number, win_prizes):
    return int(log(players_number, 2)) + int(log(win_prizes - 1, 2) if win_prizes > 1 else 0)


def get_players_position_comparator(tournament_results, tournament_games):

    def get_rival(player, game):
        return game.playing_white_player if player == game.playing_black_player else game.playing_black_player

    def get_player_games(player):
        return filter(
            lambda game: player == game.playing_white_player or player == game.playing_black_player,
            tournament_games)

    def get_player_rivals_result(player):
        player_rivals_results = []
        rivals = set([get_rival(player, game) for game in get_player_games(player)])
        for tournament_result in tournament_results:
            for rival in rivals:
                if tournament_result.player == rival:
                    player_rivals_results.append(tournament_result)
        return player_rivals_results

    def to_cmp_result(result):
        return int(result * 2)

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
            return to_cmp_result(player1_result.points - player2_result.points)

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
                return to_cmp_result(player1_rivals_points - player2_rivals_points)

        # compare ranks
        return to_cmp_result(player1.rank - player2.rank)

    return compare_players

def get_tournament_result(tournament_results, player):
    for tournament_result in tournament_results:
        if player == tournament_result.player:
            return tournament_result
    return None

def get_games_pairs(tournament_results, tournament_games):
    games = []
    auto_win_player = None
    point_groups = {}
    for tournament_result in tournament_results:
        if tournament_result.points not in point_groups:
            point_groups[tournament_result.points] = []
        point_groups[tournament_result.points].append(tournament_result)

    point_groups_seq = sorted(point_groups.keys(), reverse=True)
    players_position_comparator = get_players_position_comparator(tournament_results, tournament_games)
    for i, points in enumerate(point_groups_seq):
        players = [point_group.player for point_group in point_groups[points]]
        players.sort(cmp=players_position_comparator, reverse=True)
        if len(players) % 2 == 1:
            if i + 1 < len(point_groups_seq):
                points_in_next_groups = point_groups_seq[i + 1]
                tournament_result = get_tournament_result(tournament_results, players.pop())
                point_groups[points_in_next_groups].insert(0, tournament_result)
            else:
                auto_win_player = players.pop()
        half_point_group = len(players) / 2
        for i in xrange(half_point_group):
            games.append((players[i], players[i + half_point_group],))

    return games, auto_win_player
