from math import fabs
from chess.tournament.elo_rank import get_ranking_coefficient, get_expected_value, get_rank_change
from django.test import TestCase

from chess.tournament.models import Player, TournamentResult, Game
from chess.tournament.swiss_system import get_players_position_comparator, get_rounds_count, get_games_pairs


def create_player(id, name, rank):
    player = Player()
    player.id = id
    player.name = name
    player.rank = rank
    return player


def create_game(id, player1, player2):
    game = Game()
    game.id = id
    game.playing_white_player = player1
    game.playing_black_player = player2
    return game


def create_tournament_result(id, player, points):
    tournament_result = TournamentResult()
    tournament_result.id = id
    tournament_result.player = player
    tournament_result.points = points
    return tournament_result


class SwissSystemTest(TestCase):

    def test_getting_rounds_count(self):
        self.assertEqual(get_rounds_count(8, 1), 3)
        self.assertEqual(get_rounds_count(16, 1), 4)
        self.assertEqual(get_rounds_count(8, 4), 4)
        self.assertEqual(get_rounds_count(16, 4), 5)

    def test_creating_player_stubs(self):
        player1_0 = create_player(1, 'player1', 1000)
        player1_1 = create_player(1, 'player1', 1000)
        player2 = create_player(2, 'player2', 1000)
        self.assertEqual(player1_0, player1_1)
        self.assertNotEqual(player1_0, player2)

    def test_creating_tournament_result_stubs(self):
        player1 = create_player(1, 'player1', 1000)
        player2 = create_player(2, 'player2', 1000)
        tournament_result_player1_0 = create_tournament_result(1, player1, 10)
        tournament_result_player1_1 = create_tournament_result(1, player1, 10)
        tournament_result_player2 = create_tournament_result(2, player2, 10)
        self.assertEqual(tournament_result_player1_0, tournament_result_player1_1)
        self.assertNotEqual(tournament_result_player1_0, tournament_result_player2)
        self.assertEqual(player1, tournament_result_player1_0.player)

    def test_creating_games_stubs(self):
        player1 = create_player(1, 'player1', 1000)
        player2 = create_player(2, 'player2', 1000)
        game1_0 = create_game(1, player1, player2)
        game1_1 = create_game(1, player1, player2)
        game2 = create_game(2, player1, player2)
        self.assertEqual(game1_0, game1_1)
        self.assertNotEqual(game1_0, game2)

    def test_sort_players_with_different_points(self):
        player1 = create_player(1, 'player1', 1000)
        player2 = create_player(2, 'player2', 1000)
        results = [create_tournament_result(1, player1, 10),
                   create_tournament_result(2, player2, 20), ]

        players_comparator = get_players_position_comparator(results, [])

        sorted_players = sorted([player1, player2], cmp=players_comparator)
        self.assertEqual(sorted_players[0], player1)
        self.assertEqual(sorted_players[1], player2)

        sorted_players = sorted([player2, player1], cmp=players_comparator)
        self.assertEqual(sorted_players[0], player1)
        self.assertEqual(sorted_players[1], player2)

    def test_sort_players_with_different_ranks(self):
        player1 = create_player(1, 'player1', 1000)
        player2 = create_player(2, 'player2', 2000)
        results = [create_tournament_result(1, player1, 10),
                   create_tournament_result(2, player2, 10), ]

        players_comparator = get_players_position_comparator(results, [])

        sorted_players = sorted([player1, player2], cmp=players_comparator)
        self.assertEqual(sorted_players[0], player1)
        self.assertEqual(sorted_players[1], player2)

        sorted_players = sorted([player2, player1], cmp=players_comparator)
        self.assertEqual(sorted_players[0], player1)
        self.assertEqual(sorted_players[1], player2)

    def test_sort_players_with_different_buchholz_coefficients(self):
        player1 = create_player(1, 'player1', 2000)
        player2 = create_player(2, 'player2', 1000)
        rival1 = create_player(3, 'rival1', 1000)
        rival2 = create_player(4, 'rival2', 1000)
        games = [create_game(1, player1, rival1),
                 create_game(2, player2, rival2), ]
        results = [create_tournament_result(1, player1, 10),
                   create_tournament_result(2, player2, 10),
                   create_tournament_result(3, rival1, 10),
                   create_tournament_result(4, rival2, 20), ]

        players_comparator = get_players_position_comparator(results, games)

        sorted_players = sorted([player1, player2], cmp=players_comparator)
        self.assertEqual(sorted_players[0], player1)
        self.assertEqual(sorted_players[1], player2)

        sorted_players = sorted([player2, player1], cmp=players_comparator)
        self.assertEqual(sorted_players[0], player1)
        self.assertEqual(sorted_players[1], player2)

    def test_sort_players_with_different_buchholz_coefficients_2(self):
        player1 = create_player(1, 'player1', 2000)
        player2 = create_player(2, 'player2', 1000)
        rival1 = create_player(3, 'rival1', 1000)
        rival2 = create_player(4, 'rival2', 1000)
        rival3 = create_player(5, 'rival3', 1000)
        rival4 = create_player(6, 'rival4', 1000)
        games = [create_game(1, player1, rival1),
                 create_game(2, player1, rival2),
                 create_game(3, player2, rival3),
                 create_game(4, player2, rival4), ]
        results = [create_tournament_result(1, player1, 10),
                   create_tournament_result(2, player2, 10),
                   create_tournament_result(3, rival1, 10),
                   create_tournament_result(4, rival2, 20),
                   create_tournament_result(5, rival3, 15),
                   create_tournament_result(6, rival4, 15), ]

        players_comparator = get_players_position_comparator(results, games)

        sorted_players = sorted([player1, player2], cmp=players_comparator)
        self.assertEqual(sorted_players[0], player1)
        self.assertEqual(sorted_players[1], player2)

        sorted_players = sorted([player2, player1], cmp=players_comparator)
        self.assertEqual(sorted_players[0], player1)
        self.assertEqual(sorted_players[1], player2)

    def test_sort_players_with_different_games(self):
        player1 = create_player(1, 'player1', 2000)
        player2 = create_player(2, 'player2', 1000)
        rival1 = create_player(3, 'rival1', 1000)
        rival2 = create_player(4, 'rival2', 1000)
        rival3 = create_player(5, 'rival3', 1000)
        games = [create_game(1, player1, rival1),
                 create_game(2, player2, rival2),
                 create_game(3, player2, rival3), ]
        results = [create_tournament_result(1, player1, 10),
                   create_tournament_result(2, player2, 10),
                   create_tournament_result(3, rival1, 30),
                   create_tournament_result(4, rival2, 10),
                   create_tournament_result(5, rival3, 10), ]

        players_comparator = get_players_position_comparator(results, games)

        sorted_players = sorted([player1, player2], cmp=players_comparator)
        self.assertEqual(sorted_players[0], player1)
        self.assertEqual(sorted_players[1], player2)

        sorted_players = sorted([player2, player1], cmp=players_comparator)
        self.assertEqual(sorted_players[0], player1)
        self.assertEqual(sorted_players[1], player2)

    def test_getting_games_pairs_with_3_players(self):
        player1 = create_player(1, 'player1', 2000)
        player2 = create_player(2, 'player2', 1500)
        player3 = create_player(3, 'player2', 1000)
        results = [create_tournament_result(1, player1, 0),
                   create_tournament_result(3, player2, 0),
                   create_tournament_result(2, player3, 0), ]

        game_pairs, auto_win_player =  get_games_pairs(results, [])
        self.assertTrue(game_pairs[0][0] == player1 or game_pairs[0][1] == player1)
        self.assertTrue(game_pairs[0][0] == player2 or game_pairs[0][1] == player2)
        self.assertEqual(player3, auto_win_player)

    def test_getting_games_pairs_with_5_players(self):
        player1 = create_player(1, 'player1', 2000)
        player2 = create_player(2, 'player2', 1800)
        player3 = create_player(3, 'player3', 1500)
        player4 = create_player(4, 'player4', 1200)
        player5 = create_player(5, 'player5', 1000)
        results = [create_tournament_result(1, player5, 0),
                   create_tournament_result(2, player1, 0),
                   create_tournament_result(3, player2, 0),
                   create_tournament_result(4, player3, 0),
                   create_tournament_result(5, player4, 0), ]

        game_pairs, auto_win_player =  get_games_pairs(results, [])
        self.assertTrue(game_pairs[0][0] == player1 or game_pairs[0][1] == player1)
        self.assertTrue(game_pairs[0][0] == player3 or game_pairs[0][1] == player3)
        self.assertTrue(game_pairs[1][0] == player2 or game_pairs[1][1] == player2)
        self.assertTrue(game_pairs[1][0] == player4 or game_pairs[1][1] == player4)
        self.assertEqual(player5, auto_win_player)


class EloRankTest(TestCase):

    def test_get_ranking_coefficient(self):
        self.assertEqual(get_ranking_coefficient(1000, 10), 30)
        self.assertEqual(get_ranking_coefficient(2400, 10), 30)
        self.assertEqual(get_ranking_coefficient(3000, 10), 30)
        self.assertEqual(get_ranking_coefficient(1000, 30), 30)
        self.assertEqual(get_ranking_coefficient(2400, 30), 30)
        self.assertEqual(get_ranking_coefficient(3000, 30), 30)
        self.assertEqual(get_ranking_coefficient(1000, 31), 15)
        self.assertEqual(get_ranking_coefficient(2400, 31), 10)
        self.assertEqual(get_ranking_coefficient(3000, 31), 10)

    def test_get_expected_result(self):
        self.assertEqual(get_expected_value(1000, 1000), get_expected_value(1000, 1000))
        self.assertLess(get_expected_value(1000, 1500), get_expected_value(1500, 1000))

    def test_get_rank_change(self):
        self.assertGreater(get_rank_change(1000, 10, 1500, 1), get_rank_change(1500, 10, 1000, 1))
        self.assertGreater(get_rank_change(1000, 10, 1500, 0.5), get_rank_change(1500, 10, 1000, 0.5))
        self.assertGreater(get_rank_change(1000, 10, 1500, 0), get_rank_change(1500, 10, 1000, 0))

        self.assertGreater(fabs(get_rank_change(1000, 10, 1500, 1)), fabs(get_rank_change(1500, 10, 1000, 1)))
        self.assertLess(fabs(get_rank_change(1000, 10, 1500, 0)), fabs(get_rank_change(1500, 10, 1000, 0)))
