from all_functions import username_and_password, add_or_remove_events


def run():
    print("\n 🇦🇫🇦🇽🇦🇱🇦🇸🇦🇹🇧🇪🇨🇦🇧🇮🇧🇭🇬🇪🇬🇩🇮🇪🇲🇾🎌🇸🇨🇻🇳🇪🇭󠁧󠁢󠁷󠁬󠁳🇻🇺🇹🇨🇹🇷🇹🇳🇺🇬🇸🇲🇲🇰")
    print("\n ️🏴󠁧󠁢󠁷󠁬󠁳󠁿 🇵🇰 🎊 Welcome to Olympick App 🎊 🇮🇷 🇬🇧 \n")
    username, password = username_and_password()
    add_or_remove_events(username, password)



if __name__ == '__main__':
    run()

