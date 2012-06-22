from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=60)
    rank = models.FloatField()
    game_count = models.IntegerField(default=0)

    @property
    def all_games(self):
        return Game.objects.filter(models.Q(playing_white_player=self) |
                                   models.Q(playing_black_player=self))

    def get_all_games_in_tournament(self, tournament):
        return Game.objects.filter(models.Q(round__tournament=tournament),
                                  (models.Q(playing_white_player=self) |
                                   models.Q(playing_black_player=self)))

    def __unicode__(self):
        return u'%s (%s)' % (self.name, int(self.rank))


class Tournament(models.Model):
    TOURNAMENT_TYPE = (
        ('Swiss-system', 'Swiss-system'),
    )

    start_date = models.DateField()
    name = models.CharField(max_length=60)
    type = models.CharField(max_length=30, choices=TOURNAMENT_TYPE, default='Swiss-system')
    players = models.ManyToManyField(Player)
    win_prizes_count = models.IntegerField(default=1)

    @property
    def rounds(self):
        return self.round_set.order_by('-number').all()

    @property
    def results(self):
        return self.tournamentresult_set.all()

    def get_all_games_in_tournament(self):
        return Game.objects.filter(round__tournament=self)

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.start_date)


class TournamentResult(models.Model):
    tournament = models.ForeignKey(Tournament)
    player = models.ForeignKey(Player)
    points = models.FloatField(default=0)

    def __unicode__(self):
        return u'%s - %s' % (self.tournament, self.points)


class Round(models.Model):
    tournament = models.ForeignKey(Tournament)
    number = models.IntegerField()
    start_date = models.DateField()

    @property
    def games(self):
        return self.game_set.all()

    def __unicode__(self):
        return u'%s (%s)' % (self.tournament, self.number)


class Game(models.Model):
    GAME_RESULT = (
        ('vs', 'vs'),
        ('1:0', '1:0',),
        ('0.5:0.5', '0.5:0.5',),
        ('0:1', '0:1',),
    )

    round = models.ForeignKey(Round)
    playing_white_player = models.ForeignKey(Player, related_name='playing_white_game_set')
    playing_black_player = models.ForeignKey(Player, related_name='playing_black_game_set')
    playing_white_player_rank_change = models.FloatField(default=0)
    playing_black_player_rank_change = models.FloatField(default=0)
    result = models.CharField(max_length=10, choices=GAME_RESULT, default='vs')
    start_date = models.DateTimeField()

    def __unicode__(self):
        return u'%s %s %s' % (self.playing_white_player, self.result, self.playing_black_player)
