# show the events by getting the name of the sports
# show the events by getting the id of the sports
# show the names of events for  specific sport
# show the location of the events
import requests
from datetime import datetime, timedelta
from db_utils import verify_password, verify_existing_username, verify_new_username, remove_event_from_database, get_entire_schedule, add_event_to_database
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
            new_data = {'event_name': event, 'start_event': formatted_start_time, 'end_event': formatted_end_time}
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


def add_specific_event(result):
    inp = input("Choose the number of the event(s) you would like to add to your schedule!")
    array = []
    inp = inp.split()
    map_object = map(int, inp)
    for i in map_object:
        index = int(i) - 1
        adding_event = result[index]
        array.append(adding_event)
    return array


def remove_event(result):
    inp = input("Choose the numbers of the event(s) you would like to remove to your schedule!")
    array_remove = []
    inp = inp.split()
    map_object = map(int, inp)
    for i in map_object:
        index = int(i) - 1
        adding_event = result[index]
        array_remove.append(adding_event)
    return array_remove


def username_and_password():
    existing_user = input("Have you used our app before?").lower()
    if existing_user == 'no':
        username = input('Please choose a username')
        verify_new_username(username)
        password = input('Please choose a password')
        print("Let's add some events to your personalised Olympick schedule!")
    elif existing_user == 'yes':
        username = input('Please enter your username')
        verify_existing_username(username)
        password = input('Please enter your password')
        verify_password(username, password)
    return username, password


def add_or_remove_events(username, password):
    print("Here is your current schedule: \n")
    result = get_entire_schedule(username)
    operator = input("Would you like to: 1. Add more events or 2. Remove some events?")
    if operator == '1':
        add_events(username, password)
    elif operator == '2':
        array_remove = remove_event(result)
        remove_event_from_database(username, array_remove)
        operator = input("Would you like to\n 1. Add more events\n 2. See your schedule again\n 3. Would you like to quit?")
        if operator == '1':
            add_events(username, password)
        elif operator == '2':
            get_entire_schedule(username)
        else:
            quit()


def add_events(username, password):
    all_sports = get_all_sports()
    print("🚩🚦 The names you can choose from are : 🚦 🚩 ")
    for sport in all_sports['result']:
        print("🎖", sport['name'], "🎖")
    sport_name = input("for which sport you would like to know the schedules ? ")
    result = find_event_id_by_name(sport_name)
    print(f" 🏵🤺🤸🏻‍️🏆 All the schedules for {sport_name} : 🏆🤸🤺🏵‍")
    generator2 = (res for res in result)
    index = 0
    for res in generator2:
        index = index + 1
        print("\n", index, res['event_name'], "\nBegins at: ", res['start_event'], "\nEnds at: ", res['end_event'],
              "\n")
    array = add_specific_event(result)
    add_event_to_database(sport_name, username, array, password)


def filler(username, password):
    operator = input("Would you like to see your schedule now?")
    if operator == 'yes':
        get_entire_schedule(username)
        add_or_remove_events(username, password)
    else:
        print("See you soon!")
        quit()