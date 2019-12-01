import wave_helper

INVALID_INPUT_WAV_FILE_ERR = ('An error occurred while reading the WAV file {}.'
                              'Try Again')
WELCOME_MENU_MSG = (
    '''Welcome to the WAV editor! What would you like to do today?
1. Edit WAV
2. Compose
3. Exit
> ''')
EXIT_MENU_MSG = '''Enter output file name:
> '''
INVALID_CHOICE_ERR_FORMAT = 'Invalid choice {}'
CHOOSE_FILE_MSG = """Choose file to edit
> """
EDIT_MENU_MSG = """What would you like to do?
1. Reverse audio
2. Accelerate
3. Decelerate
4. Increase volume
5. Decrease volume
6. Low pass filter
7. Exit menu
> """
EXIT_CHOICE = '7'


def get_valid_input(input_msg, error_msg_format, predicate):
    """
    Gets a valid input from the user
    :param input_msg: The input message to display
    :param error_msg_format: The error message format to display if the input
    is invalid
    :param predicate: A predicate that returns True if the input is invalid,
    otherwise False
    :return: A valid input from the user
    """
    user_input = input(input_msg)
    # As long as the input is not valid retry
    while predicate(user_input):
        print(error_msg_format.format(user_input))
        user_input = input(input_msg)
    return user_input


def choose_file():
    """
    Makes the user choose a file to edit
    :return: None
    """
    file_name = get_valid_input(CHOOSE_FILE_MSG, INVALID_INPUT_WAV_FILE_ERR,
                                lambda f: wave_helper.load_wave(f) == -1)
    load_output = wave_helper.load_wave(file_name)
    frame_rate, audio_data = load_output
    edit_menu(frame_rate, audio_data)


def edit_menu(frame_rate, audio_data):
    """
    Enables the user to edit an existing WAV file
    :return: None
    """
    choice = get_valid_input(EDIT_MENU_MSG, INVALID_CHOICE_ERR_FORMAT,
                             lambda c: c not in EDIT_MENU)
    # Keep editing mode as long as the user does not exit
    while choice != EXIT_CHOICE:
        EDIT_MENU[choice](audio_data)
        choice = get_valid_input(EDIT_MENU_MSG, INVALID_CHOICE_ERR_FORMAT,
                                 lambda c: c not in EDIT_MENU)
    exit_menu(frame_rate, audio_data)


def compose_menu():
    print('Compose menu fucking A')


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
    '1': choose_file,
    '2': compose_menu,
    '3': quit,
}

EDIT_MENU = {
    '1': print,
    '2': print,
    '3': print,
    '4': print,
    '5': print,
    '6': print,
    EXIT_CHOICE: exit_menu,
}


def welcome_menu():
    """
    Displays the welcome menu to the user, and gets the user's choice
    :return: None
    """
    choice = get_valid_input(WELCOME_MENU_MSG, INVALID_CHOICE_ERR_FORMAT,
                             lambda c: c not in ENTER_MENU)
    ENTER_MENU[choice]()


if __name__ == '__main__':
    welcome_menu()
