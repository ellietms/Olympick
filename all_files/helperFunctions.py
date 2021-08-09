from datetime import datetime, timedelta
from collections import ChainMap
from pprint import  pprint as pp

def formattedData(nestedFunction):
    def inner_wrapper(id):
        data = nestedFunction(id)
        for eachSport in data['result']:
            event = eachSport['event']
            time_start = datetime.strptime(eachSport['start'], '%Y-%m-%d %H:%M:%S')
            time_end = datetime.strptime(eachSport['end'], '%Y-%m-%d %H:%M:%S')
            uk_time_start = time_start - timedelta(hours=8)
            uk_time_end = time_end - timedelta(hours=8)
            formatted_start_time = uk_time_start.strftime('%d %B %Y - %H:%M:%S')
            formatted_end_time = uk_time_end.strftime('%d %B %Y - %H:%M:%S')
            new_data ={'event':event , 'start':formatted_start_time , 'end':formatted_end_time}
            chain = ChainMap(new_data)
            print(chain)
    return  inner_wrapper




