import requests
import apiKey #apiKey.py with apiKey = ''
import time
import pandas as pd
import csv

# NOTE: Run prepCsv.py first to prep header row. That will delete any existing data.csv, however.

def main():
    # First set of data from a single player
    print('Getting matches for dyrus')
    matchList = getMatchList('dyrus')
    nameList = getMatchDetails(matchList)

    # New match list generated from first input name
    newMatchList = []

    # For each player, we get a new list of matches
    for player in nameList:
        print('Getting matches for ' + player)
        newMatchList.append(getMatchList(player))

    # Remove duplicate names in nameList
    nameList = list(set(nameList))
    print('New match list created')

    getMatchDetails(newMatchList)
    print('Complete')

def getMatchList(name):
    # Initial request for basic info
    response = requests.get('https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + name + '?api_key=' + apiKey.apiKey, timeout = 5)
    if response.status_code == 200:
        data = response.json()

        # Set account Id needed to get match lists
        accountId = data['accountId']

        # Get match list
        response = requests.get('https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + accountId + '?queue=420' + '&api_key=' + apiKey.apiKey, timeout = 5)
        matchList = response.json()

        return matchList
    else:
        print('getMatchList error')

def getMatchDetails(matchList):
    # Initialize returnList which is final list to be saved
    returnList = []

    # Initialize nameList which is list of names of players in these games
    nameList = []

    # For each match in the match list, append all 10 player's data to returnList object
    for match in matchList['matches']:
        print('    Getting data for match ' + str(match['gameId']))
        response = requests.get('https://na1.api.riotgames.com/lol/match/v4/matches/' + str(match['gameId']) + '?api_key=' + apiKey.apiKey, timeout = 5)
        if response.status_code == 200:
            time.sleep(5) # 5 second delay for rate limit

            data = response.json()
            for player in data['participants']:
                # print(player['participantId'])
                returnList.append(player['stats'])

            for player in data['participantIdentities']:
                nameList.append(player['player']['summonerName'])

            # Convert list of dict to pandas dataframe
            returnDf = pd.DataFrame(returnList)

            # Select only following columns
            headerList = ['win', 'item0', 'item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'perk0',	'perk0Var1',	'perk0Var2',	'perk0Var3',	'perk1',	'perk1Var1',	'perk1Var2',	'perk1Var3',	'perk2',	'perk2Var1',	'perk2Var2',	'perk2Var3',	'perk3',	'perk3Var1',	'perk3Var2',	'perk3Var3',	'perk4',	'perk4Var1',	'perk4Var2',	'perk4Var3',	'perk5',	'perk5Var1',	'perk5Var2',	'perk5Var3',	'perkPrimaryStyle',	'perkSubStyle',	'statPerk0',	'statPerk1',	'statPerk2'
            ]
            returnDf = returnDf[headerList]

            # Append to data.csv
            with open('data.csv', 'a') as f:
                returnDf.to_csv(f, index=False, header=False)
        else:
            print('getMatchDetails error on match' + match['gameId'])

    return nameList

if __name__ == "__main__":
    main()