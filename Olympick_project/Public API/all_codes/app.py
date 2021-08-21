from flask import Flask, jsonify, request
from db_utils import get_entire_schedule, add_event_to_database
from all_functions import username_and_password, add_or_remove_events, add_specific_event

app = Flask(__name__)


@app.route('/schedule/<username>')
def get_schedule_app(username):
    res = get_entire_schedule(username)
    return jsonify(res)

# http://127.0.0.1:5001/schedule/meg


@app.route('/schedule/add-booking', methods=['POST', 'GET'])
def add_event_app():
    username, password = username_and_password()
    sport, result = add_or_remove_events(username, password)
    array = add_specific_event(result)
    res = add_event_to_database(sport, username, array, password)
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True, port=5001)

