from django.db import models


# Create your models here.

# there's no id fields, because Django automatically adds them
class player(models.Model):
    email = models.CharField(max_length=254)  # 254 is max length of an email address as per RFC3696 Errata ID 1690
    password = models.CharField(max_length=256)
    nickname = models.CharField(max_length=20)
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.nickname


class game(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class team(models.Model):
    name = models.CharField(max_length=40)
    fk_game = models.ForeignKey(game, on_delete=models.CASCADE)
    fk_player = models.ForeignKey(player, on_delete=models.CASCADE)  # team leader

    def __str__(self):
        return self.name


class player_team(models.Model):
    fk_player = models.ForeignKey(player, on_delete=models.CASCADE)
    fk_team = models.ForeignKey(team, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(default=None, blank=True, null=True)

    def __str__(self):
        return f'PID({self.fk_player.id})-TID({self.fk_team.id}) ({self.start_date})-({self.end_date})'


class statistics(models.Model):
    kills = models.IntegerField()
    deaths = models.IntegerField()
    assists = models.IntegerField()
    fk_game = models.ForeignKey(game, on_delete=models.CASCADE)
    fk_player = models.ForeignKey(player, on_delete=models.CASCADE)

    def __str__(self):
        return f'Game: {self.fk_game}; Player: {self.fk_player}; KDA: {self.kills}/{self.deaths}/{self.assists}'


class location(models.Model):
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=90)
    number = models.IntegerField()
    apt_number = models.IntegerField()

    def __str__(self):
        return f'{self.postal_code} {self.city}, {self.street} {self.number}/{self.apt_number}'


class tournament(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=2000)
    start_date = models.DateField()
    end_date = models.DateField()
    fk_game = models.ForeignKey(game, on_delete=models.CASCADE)
    fk_location = models.ForeignKey(location, on_delete=models.SET_NULL, blank=True, null=True)
    fk_player = models.ForeignKey(player, on_delete=models.CASCADE)  # tournament founder/creator

    def __str__(self):
        return self.name


class team_tournament(models.Model):
    fk_tournament = models.ForeignKey(tournament, on_delete=models.CASCADE)
    fk_team = models.ForeignKey(team, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.fk_team} - {self.fk_tournament}'


class match(models.Model):
    fk_tournament = models.ForeignKey(tournament, on_delete=models.CASCADE)
    fk_team_1 = models.ForeignKey(team, on_delete=models.CASCADE, related_name='team_1')
    fk_team_2 = models.ForeignKey(team, on_delete=models.CASCADE, related_name='team_2')
    fk_prev_match_1 = models.ForeignKey('self', on_delete=models.CASCADE, related_name='prev_match_1')
    fk_prev_match_2 = models.ForeignKey('self', on_delete=models.CASCADE, related_name='prev_match_2')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    def __str__(self):
        return f'{self.fk_tournament} -> {self.fk_team_1} vs {self.fk_team_2}'


class match_statistics(models.Model):
    kills = models.IntegerField()
    deaths = models.IntegerField()
    assists = models.IntegerField()
    fk_match = models.ForeignKey(match, on_delete=models.CASCADE)
    fk_player = models.ForeignKey(player, on_delete=models.CASCADE)

    def __str__(self):
        return f'Match: {self.fk_match}; Player: {self.fk_player}; KDA: {self.kills}/{self.deaths}/{self.assists}'
