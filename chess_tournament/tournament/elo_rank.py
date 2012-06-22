def get_ranking_coefficient(player_rank, player_games_count):
    if player_games_count <= 30:
        return 30
    elif player_rank < 2400:
        return 15
    else:
        return 10


def get_expected_value(player_rank, rival_rank):
    return 1 / (1 + 10 ** (float(rival_rank - player_rank) / 400))


def get_rank_change(player_rank, player_games_count, rival_rank, player_game_result):
    ranking_coefficient = get_ranking_coefficient(player_rank, player_games_count)
    expected_value = get_expected_value(player_rank, rival_rank)
    return ranking_coefficient * (player_game_result - expected_value)