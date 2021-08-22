import requests
from datetime import datetime, timedelta
from db_utils import verify_password, verify_existing_username, verify_new_username, remove_event_from_database, \
    get_entire_schedule, add_event_to_database


# DECORATORS

# Formats event data into a more aesthetic format, and also into UK time
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
            all_data.insert(index, new_data)
        return all_data

    return inner_wrapper


# Uses the sport_id to call endpoint 2 of the API and return a list of all events and schedules for that sport.
def use_sport_id_to_return_list_of_events(nested_function):
    def inner_wrapper(sport_name):
        sport_id = nested_function(sport_name)
        get_all_specific_events = endpoint_list_of_all_events(sport_id)
        return get_all_specific_events

    return inner_wrapper


# FUNCTIONS (chronological order)

# Verifies that:
# If you are creating a new username, it does not already exist
# or
# If you are logging in with an old username, the username exists, you have inputted it correctly AND that
# you have the correct password.
# The functions within this function are all in db_utils
def username_and_password():
    existing_user = input("Have you used our app before?(Yes/No) ").lower()
    if existing_user == 'no':
        username = input('Please choose a username: ')
        verify_new_username(username)
        password = input('Please choose a password: ')
        print("Congratulations🎊!You are now one of the members of our app.")
        print("Your username is:",username)
        print("Your password is:",password)
        print("Now, Let's add some of your favourite sport's events to make your personalised olympick schedule!🎊")
        return username, password
    elif existing_user == 'yes':
        username = input('🎊It is great to see you again 🎊\nPlease enter your username to log in to the olympick app: ')
        verify_existing_username(username)
        password = input('Please enter your password: ')
        verify_password(username, password)
        print("🔐 Authentication was successful!Thank you for using our app again! ")
        return username, password
    else:
        raise ValueError("Please enter Yes or No")


# Calls endpoint 1 of the API, returns a list of all sports names (and other irrelevant details)
def list_of_all_sports():
    all_sports = 'https://olypi.com/sports/?call=GetAllSports'
    try:
        response = requests.get(all_sports)
    except Exception:
        print("Something went wrong, we are not able to retrieve all sports from the public olympic API")
    else:
        all_sports_data = response.json()
        return all_sports_data


# Uses the inputted sport name to find the sport's ID for the API (find_sport_id_by_name) - then the decorator
# uses this ID to call the API's second endpoint, to finally return a list of events within that sport.
@use_sport_id_to_return_list_of_events
def find_sport_id_by_name(sport_name):
    try:
        all_data = list_of_all_sports()
    except Exception:
        print("Sorry, something went wrong!we are not able to retrieve list of events from the public olympic API. \n please try again.")
    else:
        for sport in all_data['result']:
            if sport['name'] == sport_name:
                return sport['id']


# (This function is part of the decorator used in the above function) Calls endpoint 2 of the API, returns a list of
# all events within that sport and their schedules, which have been formatted to UK time by the decorator.
@format_data
def endpoint_list_of_all_events(sport_id):
    try:
        list_of_events = 'https://olypi.com/schedule/?call=SportEvents&id={}'.format(sport_id)
        response = requests.get(list_of_events)
        list_of_events_data = response.json()
        return list_of_events_data
    except Exception:
        print("Sorry, something went wrong!we are not able to retrieve list of sports events from the public olympic API. \n please try again.")


# Presents the entire schedule (get_entire_schedule, a function within db_utils) and then will either add_event or
# remove_event. The steps that follow either "add event" or "remove event" are discussed in further comments.

def add_or_remove_events(username, password):
    result = get_entire_schedule(username)
    operator = input("Would you like to:\n1. Add more events? \n2. Remove some events? \n3. Quit? \nYour answer: ")
    if operator == '1':
        sport_name, result = choose_sport_display_events()
        add_events(sport_name, result, username, password)
        add_or_remove_events(username, password)
    elif operator == '2':
        array_remove = remove_event(result)
        remove_event_from_database(username, array_remove)
        add_or_remove_events(username, password)
    elif operator == '3':
        print("\n💬 Thank you for using the olympick app for your ✨ personalised olympick schedule ✨!\n🤔 if you are curious about what API we are using, please find it here : https://olypi.com/\n💡 Our github for this project: https://github.com/ellietms/Olympick💡️\n❤️ We hope to see you soon again!\n 💻 Happy Coding! 💻 ")
        quit()
    else:
        print("\n***** Please enter a choice between 1, 2 or 3 *****\n")
        add_or_remove_events(username, password)


# "Add events" functionality
# Function 1/4: choose_sport_display_events
# Presents list of all sports. User can then choose a sport, which will be used to find the sport's ID by calling
# the API's second endpoint (find_sport_id_by_name) and return a list of events for that sport
# (use_sport_id_to_return_list_of_events). This list is iterated through, and each event is numbered and printed.
# This function returns the name of the sport entered, and the list of events for that sport.

def choose_sport_display_events():
    all_sports = list_of_all_sports()
    print("⚠️⚠️You can just choose between these names⚠️⚠️️")
    print("The olympic's sport names:")
    count = 1
    for sport in all_sports['result']:
        print(count,")",sport['name'], "🏆")
        count += 1
    sport_name = input("🗓 Which sport you would like to add to your personalised olympick schedule? 🗓 \n Your answer for sport name: ").title()
    result = find_sport_id_by_name(sport_name)
    print(f"\n 📣📣📣📣 The list of all events for 🔻{sport_name}🔻: 📣📣📣📣")
    generator2 = (res for res in result)
    count_event = 1
    for res in generator2:
        print(count_event,")","Event name :",res['event_name'], "\nBegins at:",res['start_event'], "\nEnds at:", res['end_event'])
        print("🔶🔸🔶🔸🔶🔸🔶🔸🔶🔸🔶🔸🔶🔸🔶🔸🔶🔸🔶🔸🔶🔸")
        count_event += 1
    return sport_name, result


# Function 2/4: add_events
# This function uses the sport's event schedule returned in the last function to call the next one (see explanation
# below).
def add_events(sport_name, result, username, password):
    array = add_specific_event(result,sport_name)
    add_event_to_database(sport_name, username, array, password)  # inside db_utils


# Function 3/4: add_specific_event
# This function will use the entire list of that sport's events (the 'result') and use zero indexing (as the function
# before presented the events as numbered) to find that event within the list of all the sports' events, and then
# add it to an array.
def add_specific_event(result,sport_name):
    add_to_database = []
    print(f"➕ Now, Let's add your favourite event(s) for 🔻{sport_name}🔻 to make your personalised olympick schedule!🎊 ➕")
    inputted_string = input("Choose the number of the event(s) from the above list that you would like to add to your schedule\n ⚠️️️ it should have spaces between the numbers you choose!(for example:1 3 20)\n Your answer: ")
    split_string = inputted_string.split()
    map_events_to_add = map(int, split_string)
    for event in map_events_to_add:
        index = int(event) - 1
        event_to_add = result[index]
        add_to_database = add_to_database + [event_to_add]
        # add_to_database.append(event_to_add)
    return add_to_database


# The fourth (4/4) "add events" function - add_event_to_database - is in the db_utils file. It uses the array
# returned in the last function, and adds all of the events individually into that user's schedule within the database.
# Further explanation is provided in the db_utils file.

# "Remove events" functionality:
# (1/2) Uses the result from get_entire_schedule (within the add_or_remove_events function), and the numbers inputted
# by the user, to index the event within the schedule and creates a list from the details of each event chosen to be
# removed.
def remove_event(result):
    print("❌ Sure, Let's remove some extra events from your personalised olympick schedule!❌")
    inputted_string = input("Choose the number of the event(s) from the above list that you would like to remove from your schedule\n ⚠️️️ it should have spaces between the numbers you choose!(for example:1 3 20)\n Your answer: ")
    remove_from_database = []
    split_string = inputted_string.split()
    map_events_to_remove = map(int, split_string)
    for event in map_events_to_remove:
        index = int(event) - 1
        event_to_remove = result[index]
        remove_from_database.append(event_to_remove)
    return remove_from_database

# The second (2/2) "remove events" function - remove_event_from_database - is in the db_utils file. It uses the array
# returned in the last function, and removes all of the events individually from that user's schedule within the
# database. Further explanation is provided in the db_utils file.
