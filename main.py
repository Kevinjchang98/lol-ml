import requests
import apiKey #apiKey.py with apiKey = ''
import time
import pandas as pd
import csv

# NOTE: Run prepCsv.py first to prep header row. That will delete any existing data.csv, however.

# NOTE: To translate from item ID to names use http://ddragon.leagueoflegends.com/cdn/9.3.1/data/en_US/item.json
# NOTE: To translate from perk ID to names use http://ddragon.leagueoflegends.com/cdn/9.3.1/data/en_US/runesReforged.json
# NOTE: To translate from champion ID to names use http://ddragon.leagueoflegends.com/cdn/9.3.1/data/en_US/champion.json

def main():
    # First set of data from a single player
    print('Getting matches for dyrus')
    matchList = getMatchList('dyrus')

    nameList = getMatchDetails(matchList)

    # Remove duplicate names in nameList
    nameList = list(set(nameList))

    # For each player, we get a new list of matches
    for player in nameList:
        print('Getting matches for ' + player)
        newMatchList = []
        newMatchList = getMatchList(player)
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
        time.sleep(120) # 2 min sleep if error occurs

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
                currentMatchDict = player['stats']
                currentMatchDict['championId'] = player['championId']

                if player['participantId'] < 6:
                    currentMatchDict['enemyChamp1'] = data['participants'][5]['championId']
                    currentMatchDict['enemyChamp2'] = data['participants'][6]['championId']
                    currentMatchDict['enemyChamp3'] = data['participants'][7]['championId']
                    currentMatchDict['enemyChamp4'] = data['participants'][8]['championId']
                    currentMatchDict['enemyChamp5'] = data['participants'][9]['championId']
                else:
                    currentMatchDict['enemyChamp1'] = data['participants'][0]['championId']
                    currentMatchDict['enemyChamp2'] = data['participants'][1]['championId']
                    currentMatchDict['enemyChamp3'] = data['participants'][2]['championId']
                    currentMatchDict['enemyChamp4'] = data['participants'][3]['championId']
                    currentMatchDict['enemyChamp5'] = data['participants'][4]['championId']

                returnList.append(currentMatchDict)


            for player in data['participantIdentities']:
                nameList.append(player['player']['summonerName'])

            # Convert list of dict to pandas dataframe
            returnDf = pd.DataFrame(returnList)

            # Select only following columns
            headerList = ['win', 'item0', 'item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'perk0','perk1','perk2','perk3','perk4','perk5','perkPrimaryStyle','perkSubStyle','statPerk0','statPerk1','statPerk2','championId','enemyChamp1','enemyChamp2','enemyChamp3','enemyChamp4','enemyChamp5']
            returnDf = returnDf[headerList]

            # Append to data.csv
            with open('data.csv', 'a') as f:
                returnDf.to_csv(f, index=False, header=False)
        else:
            print('getMatchDetails error on match' + str(match['gameId']))
            time.sleep(120) # 2 min sleep if error occurs

    return nameList

if __name__ == "__main__":
    main()