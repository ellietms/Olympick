from all_functions import find_event_id_by_name , get_all_sports
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
    sport_name = input("for which sport you would like to know the schedules ? ")
    result = find_event_id_by_name(sport_name)
    print(f" 🏵🤺🤸🏻‍️🏆 All the schedules for {sport_name} : 🏆🤸🤺🏵‍")
    pp(result)
    return result


if __name__ == '__main__':
    run()
