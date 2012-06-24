from math import log, fabs


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

def _get_tournament_result(tournament_results, player):
    for tournament_result in tournament_results:
        if player == tournament_result.player:
            return tournament_result
    return None


def _check_duplicate_game(game1_player1, game1_player2, tournament_games):
    for game in tournament_games:
        if (game1_player1 == game.playing_white_player and game1_player2 == game.playing_black_player) or\
           (game1_player1 == game.playing_black_player and game1_player2 == game.playing_white_player):
            return True
    return False

def _duplicate_game_resolver(new_round_games, auto_win_player, tournament_games):
    '''analise old games and switch new games players pairs who played before'''
    for index, new_game in enumerate(new_round_games):
        # check previous games to duplicate
        duplicate = _check_duplicate_game(new_game[0], new_game[1], tournament_games)

        index_offset = 0
        while duplicate:
            # get game offset to switch player (second player)
            index_offset = -index_offset - 1 if index_offset >=0 else -index_offset
            if index + index_offset < 0 or index + index_offset >= len(new_round_games):
                if fabs(index_offset) > len(new_round_games) - index:
                    break
                continue

            # check previous games to duplicate and change players
            change_game = new_round_games[index + index_offset]
            if not _check_duplicate_game(change_game[0], new_game[1], tournament_games) and\
               not _check_duplicate_game(new_game[0], change_game[1], tournament_games):
                change_game[1], new_game[1] = new_game[1], change_game[1]
                break

    return new_round_games, auto_win_player

def _colour_game_resolver(new_round_games, auto_win_player, tournament_games):
    '''analise old games and switch new games players colours if need'''
    players_colours = {}

    # collect player games colours statistic
    for game in tournament_games:
        if game.playing_white_player.id not in players_colours:
            players_colours[game.playing_white_player.id] = [0, 0]
        if game.playing_black_player.id not in players_colours:
            players_colours[game.playing_black_player.id] = [0, 0]

        players_colours[game.playing_white_player.id][0] += 1
        players_colours[game.playing_black_player.id][1] += 1

    # check and switch colours in games
    for new_game in new_round_games:
        if new_game[0].id not in players_colours:
            players_colours[new_game[0].id] = [0, 0]
        if new_game[1].id not in players_colours:
            players_colours[new_game[1].id] = [0, 0]

        # get players games colours counts
        player1_white = players_colours[new_game[0].id][0]
        player1_black = players_colours[new_game[0].id][1]
        player2_white = players_colours[new_game[1].id][0]
        player2_black = players_colours[new_game[1].id][1]
        delta_player1 = player1_white - player1_black
        delta_player2 = player2_white - player2_black

        # check is need change colour and switch colour
        if (fabs(delta_player1) > fabs(delta_player2) and delta_player1 > 0) or\
           (fabs(delta_player1) < fabs(delta_player2) and delta_player2 < 0) or\
           (fabs(delta_player1) == fabs(delta_player2) and (
               (delta_player1 > 0 > delta_player2) or
               (delta_player1 > 0 and delta_player2 > 0 and (
                   (player1_white > player2_white) or
                   (player1_white == player2_black and player1_black < player2_black))) or
               (delta_player1 < 0 and delta_player2 < 0 and (
                   (player1_black < player2_black) or
                   (player2_black == player2_black and player1_white > player2_white))))):
            new_game[0], new_game[1] = new_game[1], new_game[0]


    return new_round_games, auto_win_player

def get_games_pairs(tournament_results, tournament_games):
    '''analise old games and generate new games pairs'''
    games = []
    auto_win_player = None

    # get points groups
    point_groups = {}
    for tournament_result in tournament_results:
        if tournament_result.points not in point_groups:
            point_groups[tournament_result.points] = []
        point_groups[tournament_result.points].append(tournament_result)

    point_groups_seq = sorted(point_groups.keys(), reverse=True)
    players_position_comparator = get_players_position_comparator(tournament_results, tournament_games)
    for i, points in enumerate(point_groups_seq):
        # get players group and sort them
        players = [point_group.player for point_group in point_groups[points]]
        players.sort(cmp=players_position_comparator, reverse=True)

        # move last odd player in group to next group or set auto win player if this group last
        if len(players) % 2 == 1:
            if i + 1 < len(point_groups_seq):
                points_in_next_groups = point_groups_seq[i + 1]
                tournament_result = _get_tournament_result(tournament_results, players.pop())
                point_groups[points_in_next_groups].insert(0, tournament_result)
            else:
                auto_win_player = players.pop()

        # create games pairs
        half_point_group = len(players) / 2
        for i in xrange(half_point_group):
            games.append([players[i], players[i + half_point_group],])

    games, auto_win_player = _duplicate_game_resolver(games, auto_win_player, tournament_games)
    games, auto_win_player = _colour_game_resolver(games, auto_win_player, tournament_games)
    return games, auto_win_player
