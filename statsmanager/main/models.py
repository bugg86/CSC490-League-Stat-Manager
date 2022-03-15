from django.db import models

# Create your models here.
class Summoner(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    accountid = models.CharField(unique=True, max_length=100)
    puuid = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=100)
    profileIconId = models.IntegerField()
    revisiionDate = models.IntegerField()
    summonerLevel = models.IntegerField()
    
    def __str__(self):
        return self.id + ' ' + self.accountid + ' ' + \
            self.puuid + ' ' + self.name + ' ' + self.profileIconId\
                + ' ' + self.revisiionDate + ' ' + self.summonerLevel
