from all_functions import username_and_password, add_or_remove_events


def run():
    print("\n đŚđŤđŚđ˝đŚđąđŚđ¸đŚđšđ§đŞđ¨đŚđ§đŽđ§đ­đŹđŞđŹđŠđŽđŞđ˛đžđđ¸đ¨đťđłđŞđ­ó §ó ˘ó ˇó Źó łđťđşđšđ¨đšđˇđšđłđşđŹđ¸đ˛đ˛đ°")
    print("\n ď¸đ´ó §ó ˘ó ˇó Źó łó ż đľđ° đ Welcome to Olympick App đ đŽđˇ đŹđ§ \n")
    username, password = username_and_password()
    add_or_remove_events(username, password)



if __name__ == '__main__':
    run()

