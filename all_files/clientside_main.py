import requests
from helperFunctions import formattedData
from pprint import pprint as pp


# Get specific sport by id
# returns all sports names and their ids
def get_all_sports():
    all_sports = 'https://olypi.com/sports/?call=GetAllSports'
    response = requests.get(all_sports)
    all_sports_data = response.json()
    return all_sports_data

# pp(getAllSports())


# get the sports details (name  and schedule link) by it's id
def get_sports_by_id(sport_id):
    specific_sport = 'https://olypi.com/sports/?call=GetSport&id={}'.format(sport_id)
    response = requests.get(specific_sport)
    data_specific_sport = response.json()
    return data_specific_sport

# pp(getSportsById(12))


# get sports Events by their ids
@formattedData
def get_events_by_id(sport_id):
    specific_sport_event = 'https://olypi.com/schedule/?call=SportEvents&id={}'.format(sport_id)
    response = requests.get(specific_sport_event)
    data_specific_sport_event = response.json()
    return data_specific_sport_event


get_events_by_id(12)


# Get All Locations
def get_all_locations():
    all_sports_locations = 'https://olypi.com/locations/?call=GetAllLocations'
    response = requests.get(all_sports_locations)
    data_all_locations = response.json()
    return data_all_locations

# pp(getAllLocations())


# get locations by ids
def get_sport_location(sport_id):
    sport_location = 'https://olypi.com/locations/?call=GetLocation&id={}'.format(sport_id)
    response = requests.get(sport_location)
    data_location_specific_sport = response.json()
    return data_location_specific_sport

# pp(getSportLocation(20))


# get schedule
