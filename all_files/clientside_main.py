import requests
from helperFunctions import formattedData
from pprint import pprint  as pp


# Get specific sport by id
# returns all sports names and their ids
def getAllSports():
    allSports = 'https://olypi.com/sports/?call=GetAllSports'
    response = requests.get(allSports)
    allSportsData = response.json()
    return allSportsData
# pp(getAllSports())


# get the sports details (name  and schedule link) by it's id
def getSportsById(sport_id):
    specificSport = 'https://olypi.com/sports/?call=GetSport&id={}'.format(sport_id)
    response = requests.get(specificSport)
    dataSpecificSport = response.json()
    return  dataSpecificSport

# pp(getSportsById(12))



# get sports Events by their ids
@formattedData
def getEventsById(sport_id):
    specificSportEvent = 'https://olypi.com/schedule/?call=SportEvents&id={}'.format(sport_id)
    response = requests.get(specificSportEvent)
    dataSpecificSportEvent = response.json()
    return  dataSpecificSportEvent

pp(getEventsById(12))



# Get All Locations
def getAllLocations():
    allSportsLocations = 'https://olypi.com/locations/?call=GetAllLocations'
    response = requests.get(allSportsLocations)
    dataAllLocations = response.json()
    return  dataAllLocations
# pp(getAllLocations())



# get locations by ids
def getSportLocation(sport_id):
    sportLocation = 'https://olypi.com/locations/?call=GetLocation&id={}'.format(sport_id)
    response = requests.get(sportLocation)
    dataLocationSpecificSport = response.json()
    return  dataLocationSpecificSport
# pp(getSportLocation(20))


# get schedule