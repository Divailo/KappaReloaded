import dota2api
import requests
from requests.auth import HTTPDigestAuth
import json

print "==========================="

dota2ApiKey = ""

api = dota2api.Initialise(dota2ApiKey)

publicMatchesUrl = "https://api.opendota.com/api/publicMatches"
myResponse = json.loads(requests.get(publicMatchesUrl).content)
_matchIDs = []

# getting random recent matches
for match in myResponse:
	matchID = str(match['match_id'])
	print "Match Id: " + matchID
	_matchIDs.append(matchID)

_playerIDs = []

# getting players from the given matches
print "Adding palyer ids..."
for matchID in _matchIDs:
	matchUrl = "https://api.opendota.com/api/matches/" + matchID
	myResponse = json.loads(requests.get(matchUrl).content)
	try:
		for player in myResponse['players']:
			playerID = str(player['account_id'])
			if playerID != "null":
				_playerIDs.append(playerID)
			else:
				print "         PlayerID is null"
	except Exception, e:
		print "No players info for match " + matchID

# link to their steam ids so the country can be found later
_steamIds = []

for playerID in _playerIDs:
	try:
		openDotaUrl = "https://api.opendota.com/api/players/" + playerID
		myResponse = requests.get(openDotaUrl)
		steamId = str(json.loads(myResponse.content)['profile']['steamid'])
		_steamIds.append(steamId)
	except Exception, e:
		print "            NO STEAM ID FOR" + playerID


# find people from russia
_russians = []
counter = 0
idsString = ""

# make a big string of the desired ids to be found, so only one request is made
for steamID in _steamIds:
	idsString = idsString + steamID + ","

# actual getting russian players
for steamID in _steamIds:
	try:
		steamUrl = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=B54822F7D28AD07C07A21A60A0578F39&steamids=" + idsString
		myResponse = requests.get(steamUrl)
		playersArray = json.loads(myResponse.content)['response']['players']
		for playerInfo in playersArray:
			playerCountry = playerInfo['loccountrycode']
			if str(playerCountry) == "RU":
				#add to the russians list
				_russians.append(_playerIDs[counter])
				print _playerIDs[counter] + " is from" + str(playerCountry)
			else:
				print str(playerCountry)
	except Exception, e:
		print "            NO COUNTRY FOR " + steamID
	finally:
		counter = counter + 1


#wordcloud za da razbere6 kakwo pi6at naj-mnogo w 4ata
# for _id in _players:
# 	try:
# 		url = "https://api.opendota.com/api/players/" + _id + "/wordcloud"
# 		myResponse = requests.get(url)
# 		print str(json.loads(myResponse.content))
# 	except Exception, e:
# 		print "can't get wordcloud"

# stats
# https://api.opendota.com/api/players/{account_id}/counts

print "\n==========================="
print "Done!"
