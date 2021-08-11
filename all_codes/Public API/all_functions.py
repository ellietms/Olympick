# show the events by getting the name of the sports
# show the events by getting the id of the sports
# show the names of events for  specific sport
# show the location of the events
import requests
from datetime import datetime, timedelta
import collections


# JUST for seeing all sports names (without any other details) and this data is not related to schedule data
def get_all_sports():
    all_sports = 'https://olypi.com/sports/?call=GetAllSports'
    response = requests.get(all_sports)
    all_sports_data = response.json()
    return all_sports_data



# receive all the sports details with the same sport id
def get_sports_by_id(sport_id):
    specific_sport = 'https://olypi.com/sports/?call=GetSport&id={}'.format(sport_id)
    response = requests.get(specific_sport)
    data_specific_sport = response.json()
    return data_specific_sport



# decorator for formatting the current data to uk time
def format_data(nested_function):
    def inner_wrapper(*args):
        all_data = []
        data = nested_function(*args)
        index = 0
        for eachSport in data['result']:
            index += 1
            event = eachSport['event']
            time_start = datetime.strptime(eachSport['start'], '%Y-%m-%d %H:%M:%S')
            time_end = datetime.strptime(eachSport['end'], '%Y-%m-%d %H:%M:%S')
            uk_time_start = time_start - timedelta(hours=8)
            uk_time_end = time_end - timedelta(hours=8)
            formatted_start_time = uk_time_start.strftime('%d %B %Y - %H:%M:%S')
            formatted_end_time = uk_time_end.strftime('%d %B %Y - %H:%M:%S')
            new_data = {'start_event': formatted_start_time,'event_name': event,'end_event': formatted_end_time}
            all_data.insert(index,new_data)
        return all_data

    return inner_wrapper



# final result : receiving all sports events with UK time
@format_data
def get_events_by_sport_id(sport_id):
    specific_sport_event = 'https://olypi.com/schedule/?call=SportEvents&id={}'.format(sport_id)
    response = requests.get(specific_sport_event)
    data_specific_sport_event = response.json()
    return data_specific_sport_event


# decorator for just showing the event names
def get_all_names(nested_function):
    def inner_wrapper(func):
        all_names = []
        data = nested_function(func)
        for eachSport in data:
            event_name = eachSport['event_name']
            all_names.append(event_name)
        return all_names

    return inner_wrapper


#decorator for just getting the all events of the specific sport
def find_all_specific_events(nested_function):
    def inner_wrapper(sport_name):
        sport_id = nested_function(sport_name)
        get_all_specific_events = get_events_by_sport_id(sport_id)
        return get_all_specific_events

    return inner_wrapper



# get all sports Events by giving a sport name
@find_all_specific_events
def find_event_id_by_name(sport_name):
    all_data = get_all_sports()
    for sport in all_data['result']:
        if sport['name'] == sport_name:
            return sport['id']



# get just all sports names by giving a sport name
@get_all_names
@find_all_specific_events
def find_event(sport_name):
    all_data = get_all_sports()
    for sport in all_data['result']:
        if sport['name'] == sport_name:
            return sport['id']



# Get All Locations
def get_all_locations():
    all_sports_locations = 'https://olypi.com/locations/?call=GetAllLocations'
    response = requests.get(all_sports_locations)
    data_all_locations = response.json()
    return data_all_locations



# get locations by ids
def get_sport_location(sport_id):
    sport_location = 'https://olypi.com/locations/?call=GetLocation&id={}'.format(sport_id)
    response = requests.get(sport_location)
    data_location_specific_sport = response.json()
    return data_location_specific_sport


