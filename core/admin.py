from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(player)
admin.site.register(game)
admin.site.register(team)
admin.site.register(player_team)
admin.site.register(statistics)
admin.site.register(location)
admin.site.register(tournament)
admin.site.register(team_tournament)
admin.site.register(match)
admin.site.register(match_statistics)
