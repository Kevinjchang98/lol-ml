import csv

headerList = ['goldEarned', 'kills', 'deaths', 'assists', 'largestKillingSpree', 'largestMultiKill', 'killingSprees', 'longestTimeSpentLiving', 'doubleKills', 'tripleKills', 'quadraKills', 'totalHeal', 'visionScore', 'totalDamageTaken', 'turretKills', 'inhibitorKills', 'totalMinionsKilled', 'wardsPlaced', 'wardsKilled']

with open('Regression/data.csv', 'w') as f:
    csv.writer(f).writerow(headerList)
