from all_functions import endpoint_list_of_all_sports


def run():
    all_names = []
    all_sports = endpoint_list_of_all_sports()
    generator = (sport_name for sport_name in all_names)
    for sport in all_sports['result']:
        all_names.append(sport['name'])
    print("🚩 The names you can choose are : 🚩 ")
    for each_name in generator:
        print("✨", each_name, "✨")
    sport_name = input(" please choose from above names \n for which sport would you like to get the schedule link of it ?  ")
    for sport in all_sports['result']:
        if sport['name'] == sport_name:
            print(f"🗓 You can make your schedule from this link for✨ {sport_name} ✨ : ", end=" ")
            return print(sport['link'])


if __name__ == '__main__':
    run()
