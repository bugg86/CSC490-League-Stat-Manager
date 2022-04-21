from django.db import models

# Create your models here.
class Summoner(models.Model):
    id = models.CharField(primary_key=True, max_length=100, null=False)
    accountid = models.CharField(unique=True, max_length=100, null=False)
    puuid = models.CharField(unique=True, max_length=100, null=False)
    name = models.CharField(max_length=100, null=False)
    profileIconId = models.IntegerField()
    revisiionDate = models.IntegerField()
    summonerLevel = models.IntegerField()
    
    def __str__(self):
        return self.name

class Map(models.Model):
    mapid = models.IntegerField(primary_key=True, null=False)
    mapname = models.CharField(max_length=100, null=False)
    
    def __str__(self):
        return self.mapid

class Queue(models.Model):
    queueId = models.IntegerField(primary_key=True, null=False)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    description = models.CharField(max_length=4000, null=False)
    
    def __str__(self):
        return self.queueId

class Match(models.Model):
    matchId = models.CharField(primary_key=True, max_length=100)
    gameMode = models.CharField(max_length=100)
    gameDuration = models.IntegerField(null=False)
    gameName = models.CharField(max_length=100, null=False)
    gameType = models.CharField(max_length=100, null=False)
    mapId = models.IntegerField(models.ForeignKey(Map, on_delete=models.CASCADE) , null=False)
    queueId = models.IntegerField(models.ForeignKey(Queue, on_delete=models.CASCADE) , null=False)
    platformId = models.CharField(max_length=100, null=False)
    gameVersion = models.CharField(max_length=100, null=False)
    gameCreation = models.BigIntegerField(null=False)
    gameEndTimeStamp = models.BigIntegerField(null=False)
    gameStartStamp = models.BigIntegerField(null=False)
    
    def __str__(self):
        return self.matchId

class Champions(models.Model):
    championId = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=100, null=False)
    version = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=100, null=True)
    blurb = models.CharField(max_length=100, null=True)
    info_attack = models.FloatField(null=True)
    info_defense = models.FloatField(null=True)
    info_magic = models.FloatField(null=True)
    info_difficulty = models.FloatField(null=True)
    tag1 = models.CharField(max_length=25, null=True)
    tag2 = models.CharField(max_length=25, null=True)
    partype = models.CharField(max_length=25, null=True)
    stats_hp = models.FloatField(null=True)
    stats_hpperlevel = models.FloatField(null=True)
    stats_mp = models.FloatField(null=True)
    stats_mapperlevel = models.FloatField(null=True)
    stats_movespeed = models.FloatField(null=True)
    stats_armor = models.FloatField(null=True)
    stats_armorperlevel = models.FloatField(null=True)
    stats_spellblock = models.FloatField(null=True)
    stats_spellblockperlevel = models.FloatField(null=True)
    stats_attackrange = models.FloatField(null=True)
    stats_hpregen = models.FloatField(null=True)
    stats_hpregenperlevel = models.FloatField(null=True)
    stats_mpregen = models.FloatField(null=True)
    stats_mpregenperlevel = models.FloatField(null=True)
    stats_crit = models.FloatField(null=True)
    stats_critperlevel = models.FloatField(null=True)
    stats_attackdamage = models.FloatField(null=True)
    stats_attackdamageperlevel = models.FloatField(null=True)
    stats_attackspeed = models.FloatField(null=True)
    stats_attackspeedperlevel = models.FloatField(null=True)
    
    def __str__(self):
        return self.championId

class items(models.Model):
    itemId = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=100, null=True)
    cost_base = models.FloatField(null=True)
    cost_total = models.FloatField(null=True)
    cost_sell = models.FloatField(null=True)
    cost_purchaseable = models.BooleanField(null=True)
    isrune = models.BooleanField(null=True)
    description = models.CharField(max_length=4000, null=True)
    colloq = models.CharField(max_length=100, null=True)
    plaintext = models.CharField(max_length=100, null=True)
    consumed = models.BooleanField(null=True)
    stacks = models.FloatField(null=True)
    depth = models.FloatField(null=True)
    consumeonfull = models.BooleanField(null=True)
    _from = models.CharField(max_length=4000, null=True)
    _into = models.CharField(max_length=4000, null=True)
    specialrecipe = models.FloatField(null=True)
    inStore = models.BooleanField(null=True)
    hidefromall = models.BooleanField(null=True)
    requiredchampion = models.CharField(max_length=100, null=True)
    requireddaily = models.CharField(max_length=100, null=True)
    flathppoolmod = models.FloatField(null=True)
    flatmppoolmod = models.FloatField(null=True)
    flathpregenmod = models.FloatField(null=True)
    flatmpregenmod = models.FloatField(null=True)
    flatphysicaldamagemod = models.FloatField(null=True)
    flatmagicdamagemod = models.FloatField(null=True)
    flatmovementspeedmod = models.FloatField(null=True)
    percentmovementspeedmod = models.FloatField(null=True)
    percentattackspeedmod = models.FloatField(null=True)
    flatcritchancemod = models.FloatField(null=True)
    flatspellblockmod = models.FloatField(null=True)
    percentlifestealmod = models.FloatField(null=True)
    tags = models.CharField(max_length=4000, null=True)
    map1 = models.BooleanField(null=True)
    map2 = models.BooleanField(null=True)
    map3 = models.BooleanField(null=True)
    map4 = models.BooleanField(null=True)
    effects = models.CharField(max_length=4000, null=True)
    
    def __str__(self):
        return self.itemId

class MatchParticipands(models.Model):
    matchId = models.CharField(models.ForeignKey(Match, on_delete=models.CASCADE) , max_length=100, null=False)
    summonerId = models.CharField(models.ForeignKey(Summoner, on_delete=models.CASCADE) , max_length=100, null=False)
    assists = models.IntegerField(null=True)
    baronKills = models.IntegerField(null=True)
    champExperience = models.IntegerField(null=True)
    champLevel = models.IntegerField(null=True)
    championId = models.IntegerField(models.ForeignKey(Champions, on_delete=models.CASCADE) , null=True)
    championName = models.CharField(max_length=100, null=True)
    damageDealtToBuildings = models.IntegerField(null=True)
    damageDealtToObjectives = models.IntegerField(null=True)
    damageDealtToTurrets = models.IntegerField(null=True)
    damageSelfMitigated = models.IntegerField(null=True)
    deaths = models.IntegerField(null=True)
    gameEndedInSurrender = models.BooleanField(null=True)
    goldEarned = models.IntegerField(null=True)
    goldSpent = models.IntegerField(null=True)
    item0 = models.IntegerField(models.ForeignKey(items, on_delete=models.CASCADE) , null=True)
    item1 = models.IntegerField(models.ForeignKey(items, on_delete=models.CASCADE) , null=True)
    item2 = models.IntegerField(models.ForeignKey(items, on_delete=models.CASCADE) , null=True)
    item3 = models.IntegerField(models.ForeignKey(items, on_delete=models.CASCADE) , null=True)
    item4 = models.IntegerField(models.ForeignKey(items, on_delete=models.CASCADE) , null=True)
    item5 = models.IntegerField(models.ForeignKey(items, on_delete=models.CASCADE) , null=True)
    item6 = models.IntegerField(models.ForeignKey(items, on_delete=models.CASCADE) , null=True)
    kills = models.IntegerField(null=True)
    lane = models.CharField(max_length=100, null=True)
    magicDamageDealth = models.IntegerField(null=True)
    magicDamageDealthToChampions = models.IntegerField(null=True)
    participantId = models.IntegerField(null=True)
    physicalDamageDealt = models.IntegerField(null=True)
    physicalDamageDealtToChampions = models.IntegerField(null=True)
    totalHeal = models.IntegerField(null=True)
    trueDamageDealt = models.IntegerField(null=True)
    trueDamageDealtToChampions = models.IntegerField(null=True)
    win = models.BooleanField(null=True)
    id = models.IntegerField(primary_key=True, null=False)
    
    def __str__(self):
        return self.id
    
class MatchTeams(models.Model):
    matchId = models.CharField(models.ForeignKey(Match, on_delete=models.CASCADE) , max_length=100, null=False)
    teamId = models.IntegerField(null=False)
    win = models.BooleanField(null=False)
    ban1 = models.IntegerField(null=True)
    ban2 = models.IntegerField(null=True)
    ban3 = models.IntegerField(null=True)
    ban4 = models.IntegerField(null=True)
    ban5 = models.IntegerField(null=True)
    firstBaron = models.BooleanField(null=True)
    baronKills = models.IntegerField(null=True)
    firstChampion = models.BooleanField(null=True)
    championKills = models.IntegerField(null=True)
    firstDragon = models.BooleanField(null=True)
    dragonKills = models.IntegerField(null=True)
    firstInhibitor = models.BooleanField(null=True)
    inhibitorKills = models.IntegerField(null=True)
    firstRiftHerald = models.BooleanField(null=True)
    riftHeraldKills = models.IntegerField(null=True)
    firstTower = models.BooleanField(null=True)
    towerKills = models.IntegerField(null=True)
    id = models.IntegerField(primary_key=True, null=False)
    
    def __str__(self):
        return self.id

class ChampionMastery(models.Model):
    summonerId = models.CharField(models.ForeignKey(Summoner, on_delete=models.CASCADE) , max_length=100, null=False)
    championId = models.IntegerField(models.ForeignKey(Champions, on_delete=models.CASCADE) , null=True)
    championLevel = models.IntegerField(null=True)
    championPoints = models.IntegerField(null=True)
    championPointsSinceLastLevel = models.IntegerField(null=True)
    championPointsUntilNextLevel = models.IntegerField(null=True)
    chestGranted = models.BooleanField(null=True)
    tokensEarned = models.IntegerField(null=True)
    id = models.IntegerField(primary_key=True, null=False)
    
    def __str__(self):
        return self.id

class Leagues(models.Model):
    leagueId = models.CharField(max_length=100, null=False)
    queueType = models.CharField(max_length=100, null=False)
    tier = models.CharField(max_length=100, null=False)
    rank = models.CharField(max_length=100, null=False)
    summonerId = models.CharField(models.ForeignKey(Summoner, on_delete=models.CASCADE) , max_length=100, null=False)
    summonerName = models.CharField(max_length=100, null=True)
    leaguePoints = models.IntegerField(null=True)
    wins = models.IntegerField(null=True)
    losses = models.IntegerField(null=True)
    veteran = models.BooleanField(null=True)
    inactive = models.BooleanField(null=True)
    freshBlood = models.BooleanField(null=True)
    hotStreak = models.BooleanField(null=True)
    
    def __str__(self):
        return self.leagueId