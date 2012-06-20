from django.contrib import admin
from chess_tournament.tournament.models import *


class TournamentAdmin(admin.ModelAdmin):
    filter_horizontal = ('players',)


admin.site.register(Player)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(TournamentResult)
admin.site.register(Round)
admin.site.register(Game)
