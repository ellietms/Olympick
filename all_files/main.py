from all_functions  import  findEventIdByName
from pprint import pprint  as pp

def run():
    sport_name = input("What sport are you looking for ?  ")
    result = findEventIdByName(sport_name)
    print("Result of RUN function :")
    pp(result)
    return  result




if __name__ == '__main__':
    run()
