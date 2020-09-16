import csv

headerList = ['win', 'item0', 'item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'perk0',	'perk0Var1',	'perk0Var2',	'perk0Var3',	'perk1',	'perk1Var1',	'perk1Var2',	'perk1Var3',	'perk2',	'perk2Var1',	'perk2Var2',	'perk2Var3',	'perk3',	'perk3Var1',	'perk3Var2',	'perk3Var3',	'perk4',	'perk4Var1',	'perk4Var2',	'perk4Var3',	'perk5',	'perk5Var1',	'perk5Var2',	'perk5Var3',	'perkPrimaryStyle',	'perkSubStyle',	'statPerk0',	'statPerk1',	'statPerk2', 'championId', 'enemyChamp1', 'enemyChamp2', 'enemyChamp3', 'enemyChamp4', 'enemyChamp5']

with open('data.csv', 'w') as f:
    csv.writer(f).writerow(headerList)
