import requests
from pprint import pprint as pp
from datetime import datetime, timedelta


def call_endpoint1():
    endpoint1 = 'https://olypi.com/sports/?call=GetAllSports'
    response = requests.get(endpoint1)
    data = response.json()
    # print(response.status_code)
    # pp(data)
    return data


def get_sports_id(input1, data):
    for item in data['result']:
        sports_id = item['id']
        sport_name = item['name']
        if input1 == sport_name:
            return sports_id


def call_endpoint2(sports_id):
    endpoint2 = 'https://olypi.com/schedule/?call=SportEvents&id={}'.format(sports_id)
    response = requests.get(endpoint2)
    data2 = response.json()
    # print(response.status_code)
    # pp(data2)
    return data2


def return_events(data2):
    list_of_entries = []
    for item in data2['result']:
        event = item['event']
        start_of_event = item['start']
        end_of_event = item['end']
        case = {'event': event, 'start': start_of_event, 'end': end_of_event}
        list_of_entries.append(case)
        # print(str(event), str(start_of_event), str(end_of_event))
    # print(list_of_entries)
    return(list_of_entries)


def date_formatting(list_of_entries):
    list_of_formatted_entries = []
    for item in list_of_entries:
        event = item['event']
        date_obj = datetime.strptime(item['start'], '%Y-%m-%d %H:%M:%S') # now is a timestamp
        date_obj2 = datetime.strptime(item['end'], '%Y-%m-%d %H:%M:%S') # now is a timestamp
        uk_time_start = date_obj - timedelta(hours=8) # tokyo time
        uk_time_end = date_obj2 - timedelta(hours=8) # tokyo time
        formatted_start_time = uk_time_start.strftime('%d %B %Y - %H:%M:%S')
        formatted_end_time = uk_time_end.strftime('%d %B %Y - %H:%M:%S')
        case = {'event': event, 'start': formatted_start_time, 'end': formatted_end_time}
        list_of_formatted_entries.append(case)
    return list_of_formatted_entries


def present_schedule(list_of_formatted_entries):
    for item in list_of_formatted_entries:
        event = item['event']
        start = item['start']
        end = item['end']
        if 'Victory' in event:
            pass
        else:
            print("\u0332".join(event) + "\nBegins at: " + start + "\nEnds at: " + end + "\n")


def run():
    data = call_endpoint1()
    input1 = input("What sport do u want").capitalize() # is no longer case sensitive
    sports_id = get_sports_id(input1, data)
    data2 = call_endpoint2(sports_id)
    list_of_entries = return_events(data2)
    list_of_formatted_entries = date_formatting(list_of_entries)
    present_schedule(list_of_formatted_entries)


if __name__ == '__main__':
    run()



