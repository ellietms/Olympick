from all_functions import username_and_password, add_or_remove_events, filler


def run():
    print("Welcome to Olympick!")
    username, password = username_and_password()
    add_or_remove_events(username, password)
    filler(username, password)


if __name__ == '__main__':
    run()

