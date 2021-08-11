from all_functions import find_event , get_all_sports
from pprint import pprint as pp


def run():
    all_names = []
    all_sports = get_all_sports()
    generator = (sport_name for sport_name in all_names)
    for sport in all_sports['result']:
        all_names.append(sport['name'])
    print("🚩🚦 The names you can choose are : 🚦 🚩 ")
    for each_name in generator:
        print("🎖", each_name, "🎖")
    sport_name = input("for which sport you would like to know all the event's names ? ")
    print(f"ALL The event names for {sport_name} : ")
    result = find_event(sport_name)
    for eachEvent in result :
        print("🥇 event_name :" , eachEvent)
    return result


if __name__ == '__main__':
    run()
