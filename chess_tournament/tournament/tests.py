from django.test import TestCase

from chess_tournament.tournament.models import Player, TournamentResult, Game
from chess_tournament.tournament.swiss_system import get_players_position_comparator


def create_player(id, name, rank):
    player = Player()
    player.id = id
    player.name = name
    player.rank = rank
    setattr(player, '_stub_games', [])
    player.get_all_games_in_tournament = lambda tournament : getattr(player, '_stub_games')
    return player


def create_game(id, player1, player2):
    game = Game()
    game.id = id
    game.playing_white_player = player1
    game.playing_black_player = player2
    getattr(player1, '_stub_games').append(game)
    getattr(player2, '_stub_games').append(game)
    return game


def create_tournament_result(id, player, points):
    tournament_result = TournamentResult()
    tournament_result.id = id
    tournament_result.player = player
    tournament_result.points = points
    return tournament_result


class SwissSystemTest(TestCase):

    def test_creating_player_stubs(self):
        player1_0 = create_player(1, 'player1', 1000)
        player1_1 = create_player(1, 'player1', 1000)
        player2 = create_player(2, 'player2', 1000)
        self.assertEqual(player1_0, player1_1)
        self.assertNotEqual(player1_0, player2)
        self.assertEqual(player1_0.get_all_games_in_tournament(None), [])


    def test_creating_tournament_result_stubs(self):
        player1 = create_player(1, 'player1', 1000)
        player2 = create_player(2, 'player2', 1000)
        tournament_result_player1_0 = create_tournament_result(1, player1, 10)
        tournament_result_player1_1 = create_tournament_result(1, player1, 10)
        tournament_result_player2 = create_tournament_result(2, player2, 10)
        self.assertEqual(tournament_result_player1_0, tournament_result_player1_1)
        self.assertNotEqual(tournament_result_player1_0, tournament_result_player2)


    def test_creating_games_stubs(self):
        player1 = create_player(1, 'player1', 1000)
        player2 = create_player(2, 'player2', 1000)
        game = create_game(1, player1, player2)
        self.assertEqual([game], player1.get_all_games_in_tournament(None))
        self.assertEqual([game], player2.get_all_games_in_tournament(None))


    def test_sort_players_with_different_points(self):
        player1 = create_player(1, 'player1', 1000)
        player2 = create_player(2, 'player2', 1000)
        tournament_result_player1 = create_tournament_result(1, player1, 10)
        tournament_result_player2 = create_tournament_result(2, player2, 20)

        tournament_results = [tournament_result_player1, tournament_result_player2]
        players_comparator = get_players_position_comparator(None, tournament_results)

        sorted_players = sorted([player1, player2], cmp=players_comparator)
        self.assertEqual(sorted_players[0], player1)
        self.assertEqual(sorted_players[1], player2)

        sorted_players = sorted([player2, player1], cmp=players_comparator)
        self.assertEqual(sorted_players[0], player1)
        self.assertEqual(sorted_players[1], player2)


    def test_sort_players_with_different_ranks(self):
        player1 = create_player(1, 'player1', 1000)
        player2 = create_player(2, 'player2', 2000)
        tournament_result_player1 = create_tournament_result(1, player1, 10)
        tournament_result_player2 = create_tournament_result(2, player2, 10)

        tournament_results = [tournament_result_player1, tournament_result_player2]
        players_comparator = get_players_position_comparator(None, tournament_results)

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
        create_game(1, player1, rival1)
        create_game(2, player2, rival2)
        tournament_result_player1 = create_tournament_result(1, player1, 10)
        tournament_result_player2 = create_tournament_result(2, player2, 10)
        tournament_result_rival1 = create_tournament_result(3, rival1, 10)
        tournament_result_rival2 = create_tournament_result(4, rival2, 20)

        tournament_results = [tournament_result_player1, tournament_result_player2,
                              tournament_result_rival1, tournament_result_rival2]
        players_comparator = get_players_position_comparator(None, tournament_results)

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
        create_game(1, player1, rival1)
        create_game(2, player1, rival2)
        create_game(3, player2, rival3)
        create_game(4, player2, rival4)
        tournament_result_player1 = create_tournament_result(1, player1, 10)
        tournament_result_player2 = create_tournament_result(2, player2, 10)
        tournament_result_rival1 = create_tournament_result(3, rival1, 10)
        tournament_result_rival2 = create_tournament_result(4, rival2, 20)
        tournament_result_rival3 = create_tournament_result(5, rival3, 15)
        tournament_result_rival4 = create_tournament_result(6, rival4, 15)

        tournament_results = [tournament_result_player1, tournament_result_player2,
                              tournament_result_rival1, tournament_result_rival2,
                              tournament_result_rival3, tournament_result_rival4]
        players_comparator = get_players_position_comparator(None, tournament_results)

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
        create_game(1, player1, rival1)
        create_game(2, player2, rival2)
        create_game(3, player2, rival3)
        tournament_result_player1 = create_tournament_result(1, player1, 10)
        tournament_result_player2 = create_tournament_result(2, player2, 10)
        tournament_result_rival1 = create_tournament_result(3, rival1, 30)
        tournament_result_rival2 = create_tournament_result(4, rival2, 10)
        tournament_result_rival3 = create_tournament_result(5, rival3, 10)

        tournament_results = [tournament_result_player1, tournament_result_player2,
                              tournament_result_rival1, tournament_result_rival2, tournament_result_rival3]
        players_comparator = get_players_position_comparator(None, tournament_results)

        sorted_players = sorted([player1, player2], cmp=players_comparator)
        self.assertEqual(sorted_players[0], player1)
        self.assertEqual(sorted_players[1], player2)

        sorted_players = sorted([player2, player1], cmp=players_comparator)
        self.assertEqual(sorted_players[0], player1)
        self.assertEqual(sorted_players[1], player2)
