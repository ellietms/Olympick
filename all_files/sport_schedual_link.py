from all_functions import get_all_sports


def run():
    all_names = []
    all_sports = get_all_sports()
    generator = (sport_name for sport_name in all_names)
    for sport in all_sports['result']:
        all_names.append(sport['name'])
    print("🚩 The names you can choose are : 🚩 ")
    for each_name in generator:
        print("✨", each_name, "✨")
    sport_name = input(" \n for which sport would you link to get the schedule link ?  ")
    for sport in all_sports['result']:
        if sport['name'] == sport_name:
            print(f"🗓 You can make your schedule from this link for✨ {sport_name} ✨ : ", end=" ")
            return print(sport['link'])


if __name__ == '__main__':
    run()
