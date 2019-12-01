import wave_helper

WELCOME_MENU_MSG = '''Welcome to the WAV editor! What would you like to do today?
1. Edit WAV
2. Compose
3. Exit
> '''
EXIT_MENU_MSG = '''Enter output file name:
> '''
INVALID_CHOICE_ERR_FORMAT = 'Invalid choice {}'


def edit_menu():
    pass


def compose_menu():
    pass


def exit_menu(frame_rate, audio_data):
    """
    Saves the WAV data to a file
    :param audio_data: A list of lists representing the WAV file
    :param frame_rate: The frame rate of WAV file
    :return: None
    """
    output_file_name = input(EXIT_MENU_MSG)
    wave_helper.save_wave(frame_rate, audio_data, output_file_name)
    welcome_menu()


ENTER_MENU = {
    '1': edit_menu,
    '2': compose_menu,
    '3': quit
}


def welcome_menu():
    """
    Displays the welcome menu to the user, and gets the user's choice
    :return: None
    """
    choice = input(WELCOME_MENU_MSG)

    # As long as the input is not valid retry
    while choice not in ENTER_MENU:
        print(INVALID_CHOICE_ERR_FORMAT.format(choice))
        choice = input(WELCOME_MENU_MSG)
    ENTER_MENU[choice]()


if __name__ == '__main__':
    welcome_menu()
