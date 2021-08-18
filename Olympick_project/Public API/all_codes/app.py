from flask import Flask, jsonify, request
from db_utils import get_entire_schedule, add_event_to_database

app = Flask(__name__)


@app.route('/schedule/<username>')
def get_schedule_app(username):
    res = get_entire_schedule(username)
    return jsonify(res)

# http://127.0.0.1:5001/schedule/meg


# @app.route('/schedule/<username>', methods=['PUT'])
# def book_appt():
#     event_to_add = request.get_json()
#     add_event_to_database(sport=event_to_add['sport'], username=event_to_add['username'], array=event_to_add['events'], password=event_to_add['password'])
#
#     return event_to_add


if __name__ == '__main__':
    app.run(debug=True, port=5001)