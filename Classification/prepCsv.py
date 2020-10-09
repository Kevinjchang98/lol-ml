import csv

headerList = ['win', 'item0', 'item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'perk0','perk1','perk2','perk3','perk4','perk5','perkPrimaryStyle','perkSubStyle','statPerk0','statPerk1','statPerk2','championId','enemyChamp1','enemyChamp2','enemyChamp3','enemyChamp4','enemyChamp5']

with open('Classification/data.csv', 'w') as f:
    csv.writer(f).writerow(headerList)
