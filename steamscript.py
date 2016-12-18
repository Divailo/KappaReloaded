import dota2api
import requests
from requests.auth import HTTPDigestAuth
import json

dota2ApiKey = "B54822F7D28AD07C07A21A60A0578F39"

api = dota2api.Initialise(dota2ApiKey)

liveGamesCollection = api.get_live_league_games()['games']

#array of dota2 account ids
_players = []

print "==========================="

counter = 0

#loop through random n live games
while counter < 2:
	playersArray = liveGamesCollection[counter]['players']
	x = 0
	for x in playersArray:
		accountId = str(x['account_id'])
		_players.append(accountId)

	counter = counter + 1

#array of steam account ids
_steamIds = []

for _id in _players:
	try:
		openDotaUrl = "https://api.opendota.com/api/players/" + _id
		myResponse = requests.get(openDotaUrl)
		_steamId = int(json.loads(myResponse.content)['profile']['steamid'])
		_steamIds.append(_steamId)
	except Exception, e:
		print "            NO STEAM ID"
	
#map of steam accounts : country
_idCountryMap = {}
counter = 0

for _id in _steamIds:
	try:
		steamUrl = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=B54822F7D28AD07C07A21A60A0578F39&steamids=" + str(_id)
		myResponse = requests.get(steamUrl)
		playerCountry = json.loads(myResponse.content)['response']['players'][0]['loccountrycode']
		#add to the dictionary
		_idCountryMap[_players[counter]] = str(playerCountry)
	except Exception, e:
		print "            NO COUNTRY"

	counter = counter + 1

for key, value in _idCountryMap.iteritems():
	print key + " lives in " + value 



print "\n ==========================="
print "Done!"