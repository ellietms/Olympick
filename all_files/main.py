from all_functions import find_event_id_by_name
from pprint import pprint as pp


def run():
    sport_name = input("What sport are you looking for ?  ")
    result = find_event_id_by_name(sport_name)
    print("Result of RUN function :")
    pp(result)
    return result


if __name__ == '__main__':
    run()
