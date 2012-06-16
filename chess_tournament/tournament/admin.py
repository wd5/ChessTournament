from django.contrib import admin
from chess_tournament.tournament.models import *


admin.site.register(Player)
admin.site.register(Tournament)
admin.site.register(Round)
admin.site.register(Game)
