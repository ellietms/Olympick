import mysql.connector
from config import USER, PASSWORD, HOST


# Initialise Exception
class DbConnectionError(Exception):
    pass


# Function to connect to the database
def _connect_to_db(db_name):
    cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin='mysql_native_password',
        database=db_name
    )
    return cnx

# Creates connection and cursor.
# Queries the database for all records that have the username that a user has inputted.
# Records (the user's schedule) return as a list of tuples. This is iterated through and formatted to present to the
# user.
# Cursor only needs to execute one query.
# The function returns the schedule (as a list of tuples).
def get_entire_schedule(username):
    try:
        db_name = 'olympick'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        # print("Connected to DB: %s" % db_name) # uncomment this line when debugging to verify connection

        query = """
            SELECT  sport, event, beginning, end
            FROM schedule
            WHERE username = '{}'
            """.format(username)

        cur.execute(query)

        schedule = cur.fetchall()
        event_number = 1
        print(f"\n 🗓📆 Your current personalised olympick schedule 🗓📆: \n")
        if not schedule:
            schedule = 'Your schedule is empty'
        else:
            for event in schedule:
                event = list(event)
                print("🔷🔹🔷🔹🔷🔹🔷🔹🔷🔹🔷🔹🔷🔹🔷🔹🔷🔹🔷🔹🔷🔹")
                print(event_number,")","Event name:",event[1], "(🔻{}🔻)".format(event[0]), "\nBegins at: ", event[2], "\nEnds at: ", event[3])
                event_number += 1
            cur.close()

    except Exception:
        raise DbConnectionError("Sorry, we are not able to read data from database, please try again!")

    finally:
        if db_connection:
            db_connection.close()
    return schedule

# Creates connection and cursor.
# Uses the list of events to remove from a previous function.
# This list is iterated through and each event name is added to another list.
# The cursor executes many queries, removing each event in the list from the schedule of the current user.
def remove_event_from_database(username, array_remove):
    try:
        db_name = 'olympick'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        # print("Connected to DB: %s" % db_name)

        records_to_remove = []
        for i in range(len(array_remove)):
            records_to_remove.append([array_remove[i][1]])

        query = """
            DELETE FROM schedule
            WHERE username = '{}' and event = (%s);
            """.format(username)
        cur.executemany(query, records_to_remove)
        db_connection.commit()
        print("Event(s) successfully removed.")

        cur.close()

    except Exception:
        raise DbConnectionError("Sorry, we are not able to read data from database, please try again!")

    finally:
        if db_connection:
            db_connection.close()

# Creates connection and cursor.
# Uses the list of events to add from a previous function.
# This list is iterated through and each event's details is added to another list (records_to_add).
# The cursor executes many queries, adding each event (and its details) in the list to the schedule of the current user.
def add_event_to_database(sport, username, array, password):
    try:
        db_name = 'olympick'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()

        records_to_add = []
        for i in range(len(array)):
            records_to_add.append([username, sport, array[i]['event_name'], array[i]['start_event'], array[i]['end_event'], password])


        query = """
            INSERT INTO schedule
            (username, sport, event, beginning, end, password)
            VALUES (%s, %s, %s, %s, %s, %s);
            """

        cur.executemany(query, records_to_add)
        db_connection.commit()
        cur.close()
        print("Event(s) successfully added.")

    except Exception:
        raise DbConnectionError("Please choose a number in the schedule of events!")

    finally:
        if db_connection:
            db_connection.close()


# Creates connection and cursor.
# Queries the database to return all usernames.
# These usernames are iterated through to see if the inputted username already exists within them.
# The user is allowed to continue if the username does not yet exist.
def verify_new_username(username):
    try:
        db_name = 'olympick'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()


        query = """
            SELECT  username
            FROM schedule
            """

        cur.execute(query)

        usernames = cur.fetchall()
        for database_username in usernames:
            database_username = str(list(database_username))
            if username in database_username:
                print('Sorry this username is already exist, please use another username')
                quit()
            else:
                pass
        cur.close()

    except Exception:
        raise DbConnectionError("Sorry we are not able to read data from olympic's database, please try again!")

    finally:
        if db_connection:
            db_connection.close()


    return username


# Creates connection and cursor.
# Queries the database to return all usernames.
# These usernames are iterated through to see if the inputted username already exists within it. The user is allowed
# to continue if the username exists.
def verify_existing_username(username):
    try:
        db_name = 'olympick'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()


        query = """
            SELECT  username
            FROM schedule
            """

        cur.execute(query)

        usernames = cur.fetchall()
        while True:
            for database_username in usernames:
                database_username = str(list(database_username))
                if username in database_username:
                    print("🎊This username has been verified successfully!🎊")
                    return
            print("Sorry, this username doesn't exist, please make sure you are using the right username.")
            return False, quit()
        cur.close()

    except Exception:
        raise DbConnectionError("Sorry we are not able to read data from olympic's database, please try again!")

    finally:
        if db_connection:
            db_connection.close()


    return username


# Creates connection and cursor.
# Queries the database to return the password of the user with the inputted username.
# Password(s) (as they are saved in multiple records within the database) are iterated through, to see if the inputted
# password matches.
def verify_password(username, password):
    try:
        db_name = 'olympick'
        db_connection = _connect_to_db(db_name) # create database connection from sqlconnector module
        cur = db_connection.cursor() # creates the cursor
        # print("Connected to DB: %s" % db_name)

        query = """
            SELECT  password
            FROM schedule
            WHERE username = '{}'
            """.format(username)

        cur.execute(query)

        actual_password = cur.fetchall()
        for database_password in actual_password:
            database_password = str(list(database_password))
            if password in database_password:
                pass
            else:
                print("Sorry the password is not correct, please try again!")
                quit()
        print("✅ Password is correct.")
        cur.close()

    except Exception:
        raise DbConnectionError("Sorry we are not able to read data from olympic's database, please try again!")

    finally:
        if db_connection:
            db_connection.close()


    return password
