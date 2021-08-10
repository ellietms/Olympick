# show the events by getting the name of the sports
# show the events by getting the id of the sports
# show the location of the events
import requests
from pprint import pprint  as pp
from datetime import datetime, timedelta


# JUST for seeing all sports names (without any other details)
def getAllSports():
    allSports = 'https://olypi.com/sports/?call=GetAllSports'
    response = requests.get(allSports)
    allSportsData = response.json()
    return allSportsData

pp(getAllSports())



# get all the sports details with the same id ( it can be different sports but they might have same ids)
def getSportsById(sport_id):
    specificSport = 'https://olypi.com/sports/?call=GetSport&id={}'.format(sport_id)
    response = requests.get(specificSport)
    dataSpecificSport = response.json()
    return  dataSpecificSport

pp(getSportsById(12))



def formattedData(nestedFunction):
    def inner_wrapper(*args):
        all_data = []
        data = nestedFunction(*args)
        for eachSport in data['result']:
            event = eachSport['event']
            time_start = datetime.strptime(eachSport['start'], '%Y-%m-%d %H:%M:%S')
            time_end = datetime.strptime(eachSport['end'], '%Y-%m-%d %H:%M:%S')
            uk_time_start = time_start - timedelta(hours=8)
            uk_time_end = time_end - timedelta(hours=8)
            formatted_start_time = uk_time_start.strftime('%d %B %Y - %H:%M:%S')
            formatted_end_time = uk_time_end.strftime('%d %B %Y - %H:%M:%S')
            new_data ={'event':event , 'start':formatted_start_time , 'end':formatted_end_time}
            all_data.append(new_data)
        return all_data
    return  inner_wrapper


# get sports Events by their ids
@formattedData
def getEventsById(sport_id):
    specificSportEvent = 'https://olypi.com/schedule/?call=SportEvents&id={}'.format(sport_id)
    response = requests.get(specificSportEvent)
    dataSpecificSportEvent = response.json()
    return  dataSpecificSportEvent

pp(getEventsById(12))




# def formattedData2(nestedFunction):
#     def inner_wrapper():
#         all_data = []
#         data = nestedFunction()
#         for eachSport in data['result']:
#             event = eachSport['event']
#             time_start = datetime.strptime(eachSport['start'], '%Y-%m-%d %H:%M:%S')
#             time_end = datetime.strptime(eachSport['end'], '%Y-%m-%d %H:%M:%S')
#             uk_time_start = time_start - timedelta(hours=8)
#             uk_time_end = time_end - timedelta(hours=8)
#             formatted_start_time = uk_time_start.strftime('%d %B %Y - %H:%M:%S')
#             formatted_end_time = uk_time_end.strftime('%d %B %Y - %H:%M:%S')
#             new_data ={'event':event , 'start':formatted_start_time , 'end':formatted_end_time}
#             all_data.append(new_data)
#         return all_data
#     return  inner_wrapper

def findTheSportByName(nestedFunction):
    def inner_wrapper(sport_name):
        get_sport_id = nestedFunction(sport_name)
        getAllSpecificEvents = getEventsById(get_sport_id)
        print("All events",getAllSpecificEvents)
        return  getAllSpecificEvents
    return  inner_wrapper


# get sports Events by their names
# @formattedData2
@findTheSportByName
def findEventByName(sport_name):
    all_data = getAllSports()
    for sport in all_data['result']:
        if sport['name'] == sport_name:
           return sport['id']
print("ALL THE RESULTS OF SPECIFIC NAME")
pp(findEventByName('3x3 Basketball'))




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