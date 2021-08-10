# show the events by getting the name of the sports
# show the events by getting the id of the sports
# show the location of the events
import requests
from pprint import pprint  as pp
from datetime import datetime, timedelta


# JUST for seeing all sports names (without any other details) and this data is not related to schedule data
def get_all_sports():
    all_sports = 'https://olypi.com/sports/?call=GetAllSports'
    response = requests.get(all_sports)
    all_sports_data = response.json()
    return all_sports_data


# pp(get_all_sports())


# get all the sports details with the same sport id ( it can be different sports but they might have same ids)
def get_sports_by_id(sport_id):
    specific_sport = 'https://olypi.com/sports/?call=GetSport&id={}'.format(sport_id)
    response = requests.get(specific_sport)
    data_specific_sport = response.json()
    return data_specific_sport


# print("///////////////")
# print("Just get all the sports by specific id")
# pp(get_sports_by_id(12))
# print("======End======")

# get the specific sport id and return the events for that sport id( it can be different sport but with the same
# sport_id)
def formatted_data(nested_function):
    def inner_wrapper(*args):
        all_data = []
        data = nested_function(*args)
        for eachSport in data['result']:
            event = eachSport['event']
            time_start = datetime.strptime(eachSport['start'], '%Y-%m-%d %H:%M:%S')
            time_end = datetime.strptime(eachSport['end'], '%Y-%m-%d %H:%M:%S')
            uk_time_start = time_start - timedelta(hours=8)
            uk_time_end = time_end - timedelta(hours=8)
            formatted_start_time = uk_time_start.strftime('%d %B %Y - %H:%M:%S')
            formatted_end_time = uk_time_end.strftime('%d %B %Y - %H:%M:%S')
            new_data = {'event': event, 'start': formatted_start_time, 'end': formatted_end_time}
            all_data.append(new_data)
        return all_data

    return inner_wrapper


# Result : get all sports Events for one specific id
@formatted_data
def get_events_by_sport_id(sport_id):
    specific_sport_event = 'https://olypi.com/schedule/?call=SportEvents&id={}'.format(sport_id)
    response = requests.get(specific_sport_event)
    data_specific_sport_event = response.json()
    return data_specific_sport_event


# print("///////////////")
# print("show all the different sport events for specific sport id")
# pp(get_events_by_sport_id(12))
# print("===End===")


def get_all_names(nested_function):
    def inner_wrapper(func):
        all_names = []
        data = nested_function(func)
        for eachSport in data:
            event_name = eachSport['event']
            all_names.append(event_name)
        return all_names

    return inner_wrapper


def find_all_specific_events(nested_function):
    def inner_wrapper(sport_name):
        sport_id = nested_function(sport_name)
        get_all_specific_events = get_events_by_sport_id(sport_id)
        print("All events for this id is : ", end="")
        pp(get_all_specific_events)
        return get_all_specific_events

    return inner_wrapper


# get sports Events by their names
@get_all_names
@find_all_specific_events
def find_event_id_by_name(sport_name):
    all_data = get_all_sports()
    for sport in all_data['result']:
        if sport['name'] == sport_name:
            print(f"for {sport_name} id is {sport['id']}")
            return sport['id']


# print("///////////////")
# print("ALL THE RESULTS OF SPECIFIC NAME")
# pp(find_event_id_by_name('3x3 Basketball'))
# print("///////////////")


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

# pp(get_sport_location(20))


# get schedule
