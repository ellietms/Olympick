import mysql.connector
from config import USER, PASSWORD, HOST


class DbConnectionError(Exception):
    pass


def _connect_to_db(db_name):
    cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin='mysql_native_password',
        database=db_name
    )
    return cnx

def get_entire_schedule(username):
    try:
        db_name = 'olympick'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        # print("Connected to DB: %s" % db_name)

        query = """
            SELECT  sport, event, beginning, end
            FROM schedule
            WHERE username = '{}'
            """.format(username)

        cur.execute(query)

        schedule = cur.fetchall()  # this is a list with db records where each record is a tuple
        index = 0
        for i in schedule:
            i = list(i)
            index = index + 1
            print(index, i[1], "({})".format(i[0]), "\nBegins at: ", i[2], "\nEnds at: ", i[3], "\n")
        cur.close()

    except Exception:
        raise DbConnectionError("Failed to read data from DB")

    finally:
        if db_connection:
            db_connection.close()
            # print("DB connection is closed")
    return schedule


def remove_event_from_database(username, array_remove):
    try:
        db_name = 'olympick'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        # print("Connected to DB: %s" % db_name)

        records_to_remove = []
        for i in range(len(array_remove)):
            # print(array_remove)
            # print(i)
            list1 = [array_remove[i][1]]
            # print(list1)
            records_to_remove.append(list1)

        query = """
            DELETE FROM schedule
            WHERE username = '{}' and event = (%s);
            """.format(username)
        # print(query)
        cur.executemany(query, records_to_remove)
        db_connection.commit()
        print("Event(s) successfully removed.")

        cur.close()

    except Exception:
        raise DbConnectionError("Failed to read data from DB")

    finally:
        if db_connection:
            db_connection.close()
            # print("DB connection is closed")
    # return schedule

def add_event_to_database(sport, username, array, password):
    try:
        db_name = 'olympick'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        # print("Connected to DB: %s" % db_name)

        records_to_add = []
        for i in range(len(array)):
            list1 = [username, sport, array[i]['event_name'], array[i]['start_event'], array[i]['end_event'], password]
            # print(list1)
            records_to_add.append(list1)

        # print(records_to_add)

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
        raise DbConnectionError("Failed to read data from DB")

    finally:
        if db_connection:
            db_connection.close()
            # print("DB connection is closed")


def verify_new_username(username):
    try:
        db_name = 'olympick'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        # print("Connected to DB: %s" % db_name)

        query = """
            SELECT  username
            FROM schedule
            """

        cur.execute(query)

        usernames = cur.fetchall()  # this is a list with db records where each record is a tuple
        # print(actual_password)# this is a list with db records where each record is a tuple
        for i in usernames:
            i = str(list(i))
            if username in i:
                print('Sorry that username already exists')
                quit()
            else:
                pass
        cur.close()

    except Exception:
        raise DbConnectionError("Failed to read data from DB")

    finally:
        if db_connection:
            db_connection.close()
            # print("DB connection is closed")

    return username


def verify_password(username, password):
    try:
        db_name = 'olympick'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        # print("Connected to DB: %s" % db_name)

        query = """
            SELECT  password
            FROM schedule
            WHERE username = '{}'
            """.format(username)

        cur.execute(query)

        actual_password = cur.fetchall()
        # print(actual_password)# this is a list with db records where each record is a tuple
        for i in actual_password:
            i = str(list(i))
            if password in i:
                pass
            else:
                print("Incorrect password")
                quit()
        print("Password correct.")
        cur.close()

    except Exception:
        raise DbConnectionError("Failed to read data from DB")

    finally:
        if db_connection:
            db_connection.close()
            # print("DB connection is closed")

    return password


def verify_existing_username(username):
    try:
        db_name = 'olympick'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        # print("Connected to DB: %s" % db_name)

        query = """
            SELECT  username
            FROM schedule
            """

        cur.execute(query)

        usernames = cur.fetchall()  # this is a list with db records where each record is a tuple
        # print(usernames)
        for i in usernames:
            i = str(list(i))
            if username in i:
                pass
            else:
                print("This username does not exist.")
                quit()
        cur.close()

    except Exception:
        raise DbConnectionError("Failed to read data from DB")

    finally:
        if db_connection:
            db_connection.close()
            # print("DB connection is closed")

    return username
