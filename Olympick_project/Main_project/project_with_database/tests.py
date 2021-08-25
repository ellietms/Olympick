from unittest import TestCase, main
from unittest.mock import patch
from use_functions_for_tests import list_of_all_sports, find_sport_id_with_name, list_of_all_events, find_sport_id_by_name

#Creating a mock data for checking the data we get from the olympic public API
class TestListOfAllSportsFromPublicApi(TestCase):
    @patch('use_functions_for_tests.list_of_all_sports')
    def test_list_of_all_sport_for_first_item(self, mock_data):
        mock_data.return_value.json.return_value = {
            "result": [
                {
                    "id": 1,
                    "name": "Opening and Closing Ceremonies",
                    "link": "/tokyo-2020/en/schedule/ceremony-schedule#20210723_CER"
                }
            ]
        }
        result_function = list_of_all_sports()
        # the list_of_all_sports function use exceptions , so we needed to check them here
        if result_function:
            self.assertEqual(result_function.json()['result'][0]['name'],"Opening and Closing Ceremonies")
        else:
            self.assertRaises(Exception, list_of_all_sports, "Something went wrong, we are not able to retrieve all sports from the public olympic API" )



    @patch('use_functions_for_tests.list_of_all_sports')
    def test_list_of_all_sport_for_another_item(self, mock_data):
        mock_data.return_value.json.return_value = {
            "result": [
                {
                    "id": 32,
                    "name": "Rugby",
                    "link": "/tokyo-2020/en/schedule/rugby-schedule/"
                }
            ]
        }
        result_function = list_of_all_sports()
        # the list_of_all_sports function use exceptions , so we needed to check them here
        if result_function:
            self.assertEqual(result_function.json()['result'][0]['name'], "Rugby")
        else:
            self.assertRaises(Exception, list_of_all_sports,
                              "Something went wrong, we are not able to retrieve all sports from the public olympic API")



class TestFindSportIdWithName(TestCase):
    @patch('use_functions_for_tests.find_sport_id_with_name')
    def test_find_sport_id_with_name(self, mock_data):
        mock_data.return_value.json.return_value = {
            "result": [
                {
                        "id": 44,
                        "name": "Volleyball",
                        "link": "/tokyo-2020/en/schedule/volleyball-schedule/"
                }
            ]
        }
        result_function = find_sport_id_with_name("Volleyball")
        if result_function:
            self.assertEqual(result_function.json()['result'][0]['id'], 44)

        else:
            self.assertRaises(Exception, find_sport_id_with_name, "Sorry, something went wrong! We are not able to retrieve the list of events from the public olympic API. \n Please try again.")




class TestGetListOfAllSpecificSportEvents(TestCase):
    @patch('use_functions_for_tests.list_of_all_events')
    def test_find_list_of_all_specific_sport_events_by_specific_id(self, mock_data):
        mock_data.return_value.json.return_value = {
            "result": [
                {
                    "id": 473,
                    "sport_id": 10,
                    "event": "Men's or Women's Preliminaries (4 matches)",
                    "location_id": 37,
                    "start": "2021-07-24 09:00:00",
                    "end": "2021-07-24 12:50:00",
                    "start_utc": "2021-07-23 23:00:00",
                    "end_utc": "2021-07-24 02:50:00",
                    "completed": "true",
                    "is_medal": "false",
                    "is_final": "false",
                    "is_ceremony": "false"
                },
                {
                    "id": 473,
                    "sport_id": 10,
                    "event": "Men's or Women's Preliminaries (4 matches)",
                    "location_id": "null",
                    "start": "2021-07-25 09:00:00",
                    "end": "2021-07-25 12:50:00",
                    "start_utc": "2021-07-24 23:00:00",
                    "end_utc": "2021-07-25 02:50:00",
                    "completed": "false",
                    "is_medal": "false",
                    "is_final": "false",
                    "is_ceremony": "false"
                }
            ]
        }
        result_function = list_of_all_events(10)
        if result_function:
            self.assertEqual(result_function.json()['result'][0]['event'], "Men's or Women's Preliminaries (4 matches)")
            self.assertEqual(result_function.json()['result'][1]['event'], "Men's or Women's Preliminaries (4 matches)")
        else:
            self.assertRaises(Exception, find_sport_id_with_name, "Sorry, something went wrong! We are not able to retrieve list of sports events from the public olympic API. \n please try again.")



# Test of the complicated decorators( a decoratore which includes another decoratore inside of it)

class TestGetSportEventsByName(TestCase):
    @patch('use_functions_for_tests.find_sport_id_by_name')
    def test_find_sport_id_by_name(self, mock_data):
        mock_data.return_value.json.return_value = {
           "result": [
                       { 'start_event': '08 August 2021 - 03:30',
                       'event_name': "Women's Gold Medal Game",
                       'end_event': '08 August 2021 - 06:00'
                        },
                       { 'start_event': '08 August 2021 - 03:30',
                        'event_name': "Women's Victory Ceremony",
                        'end_event': '08 August 2021 - 06:00'
                       }
                ]
        }
        result_function = find_sport_id_by_name("Basketball")
        data_lists =[]
        def check_data(data):
            index = 0
            for each_data in data['result']:
                if each_data['event_name'] == mock_data["result"][index]['event_name']:
                    data_lists.append(each_data)
                    index += 1
            return data_lists
        if result_function:
            data = result_function.json()
            filtered_data = check_data(data)
            index = 0
            while index < len(filtered_data):
                for each_event in filtered_data:
                    self.assertEqual(each_event['event_name'], mock_data["result"][index]['event_name'])
                    index += 1
        else:
            self.assertRaises(Exception, find_sport_id_with_name, "Sorry, something went wrong! We are not able to retrieve the list of events from the public olympic API.")



if __name__ == "__main__":
    main()

