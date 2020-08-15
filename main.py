import requests
import apiKey #apiKey.py with apiKey = ''
import time
import pandas as pd

#TODO: Deal with possible errors in get requests

# Initialize returnList which is final list to be saved
returnList = []

# Initial request for basic info
response = requests.get('https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/dyrus?api_key=' + apiKey.apiKey, timeout = 5)
data = response.json()

# Set account Id needed to get match lists
accountId = data['accountId']

# Get match list
response = requests.get('https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + accountId + '?api_key=' + apiKey.apiKey, timeout = 5)
data = response.json()

# For each match in the match list, append all 10 player's data to returnList object
for match in data['matches'][:5]:
    print('Match ID: ' + str(match['gameId']))
    response = requests.get('https://na1.api.riotgames.com/lol/match/v4/matches/' + str(match['gameId']) + '?api_key=' + apiKey.apiKey, timeout = 5)
    time.sleep(2) # 2 second delay for rate limit

    data = response.json()
    for player in data['participants']:
        # print(player['participantId'])
        returnList.append(player['stats'])

# Save returnList as test.txt
f = open('test.txt', 'w')
f.write(str(returnList))
f.close()