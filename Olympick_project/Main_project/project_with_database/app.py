from flask import Flask, render_template, request, session
import all_functions
import db_utils
import bcrypt


app = Flask(__name__)
app.secret_key = "secret key"

@app.route('/')
def login_or_create_user():
    return render_template('login_or_not.html')


@app.route('/old_user') # used app before
def log_in():
    return render_template('login.html')

@app.route('/login', methods=['POST']) # have used app before
def existing_user():
    username = request.form['inputUserName']
    password = request.form['inputPassword']
    if db_utils.verify_existing_username(username) and db_utils.verify_password(username, password):
        session['username'] = username
        session['password'] = password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        session['hashed_password'] = hashed_password
        return render_template('choose_to_view_schedule.html')
    else:
        return render_template('incorrect_username_or_password.html')


@app.route('/schedule')
def show_schedule():
    username = session.get('username')
    schedule = db_utils.get_entire_schedule(username)
    session['schedule'] = schedule
    schedule = db_utils.get_entire_schedule(username)
    index = 0
    list_of_events = []
    if schedule == 'Your schedule is empty':
        return render_template('schedule_empty.html')
    else:
        for res in schedule:
            index = index + 1
            list_of_events.append([str(index), res[0], res[1], res[2]])
    return render_template("schedule.html", data=list_of_events)

@app.route('/new_user')
def add_user_view():
    return render_template('add_new_user.html')

@app.route('/add_new_user', methods=['POST'])
def add_user():
    username = request.form['inputUserName']
    password = request.form['inputPassword']
    session['username'] = username
    if not db_utils.verify_new_username(username):
        return render_template('username_already_exists.html')
    else:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        session['hashed_password'] = hashed_password
        session['password'] = password
        return render_template('choose_to_view_schedule.html')



@app.route('/add_new_event', methods=['GET', 'POST'])
def add_new_event_app():
    all_sports = all_functions.list_of_all_sports()
    sports_and_their_numbers = []
    index = 1
    for sport in all_sports['result']:
        sports_and_their_numbers.append([index, sport['name']])
        index += 1
    return render_template('show_sports.html', data=sports_and_their_numbers)


@app.route('/show_sports', methods=['GET', 'POST'])
def display_events():
    sport_name = request.form['inputSportName']
    session['sport_name'] = sport_name
    result = all_functions.find_sport_id_by_name(sport_name)
    session['result'] = result
    index = 0
    list_of_events = []
    for res in result:
        index = index + 1
        list_of_events.append([str(index), res['event_name'], res['start_event'],  res['end_event']])
    return render_template('show_events.html', data=list_of_events)

@app.route('/show_events', methods=['GET', 'POST'])
def events_added():
    hashed_password = session.get('hashed_password')
    sport_name = session.get('sport_name')
    input_app = request.form['inputEventNumbers']
    result = session.get('result')
    split_string = input_app.split()
    map_events_to_add = map(int, split_string)
    add_to_database = []
    for event in map_events_to_add:
        index = int(event) - 1
        event_to_add = result[index]
        add_to_database.append(event_to_add)
    username = session.get('username')
    db_utils.add_event_to_database(sport_name, username, add_to_database, hashed_password)
    schedule = db_utils.get_entire_schedule(username)
    index = 0
    list_of_events = []
    if schedule == 'Your schedule is empty':
        return render_template('schedule_empty.html')
    else:
        print(schedule)
        for res in schedule:
            index = index + 1
            list_of_events.append([str(index), res[0], res[1], res[2]])
    return render_template("schedule.html", data=list_of_events)

@app.route('/display_events_to_remove', methods=['GET', 'POST'])
def display_events_to_remove():
    username = session.get('username')
    schedule = db_utils.get_entire_schedule(username)
    index = 0
    list_of_events = []
    for res in schedule:
        index = index + 1
        list_of_events.append([str(index), res[0], res[1],  res[2]])
    return render_template('show_events_to_remove.html', data=list_of_events)

@app.route('/remove_events', methods=['GET', 'POST'])
def events_removed():
    input_app = request.form['inputEventNumbers']
    username = session.get('username')
    schedule = db_utils.get_entire_schedule(username)
    split_string = input_app.split()
    map_events_to_remove = map(int, split_string)
    remove_from_database = []
    for event in map_events_to_remove:
        index = int(event) - 1
        event_to_remove = schedule[index]
        remove_from_database.append(event_to_remove)
    db_utils.remove_event_from_database(username, remove_from_database)
    schedule = db_utils.get_entire_schedule(username)
    index = 0
    list_of_events = []
    for res in schedule:
        index = index + 1
        list_of_events.append([str(index), res[0], res[1], res[2]])
    return render_template("schedule.html", data=list_of_events)


if __name__ == '__main__':
    app.run(debug=True, port=5000)