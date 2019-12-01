import os
import re
import math
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
INVALID_INPUT_DIRECTIONS_FILE_ERR_FORMAT = 'Invalid instruction file path {}'
COMPOSE_MENU_MSG = """Enter composition directions file
> """
INCREASE_VOLUME = 1.2
DECREASE_VOLUME = 1.2
MINIMUM_VOLUME = -32768
MAXIMUM_VOLUME = 32767
SAMPLE_RATE = 2000
NUM_TO_SECONDS = 1 / 16
NOTE_TO_FREQ = {
    'A': 440,
    'B': 494,
    'C': 523,
    'D': 587,
    'E': 659,
    'F': 698,
    'G': 784
}
QUITE_NOTE = 'Q'


def reverse_audio(audio_data):
    """
    reverses the given audio data
    :param audio_data: the audio data
    :return: the reversed audio_data
    """
    audio_data.reverse()
    return list(audio_data)


def accelerate_audio(audio_data):
    """
    accelerate the audio, removes all even places of the list
    :param audio_data: the audio data
    :return: the accelerated of audio_data
    """
    return [audio for audio in audio_data[::2]]


def decelerate_audio(audio_data):
    """
    decelerates the data by adding the average between each data
    :param audio_data: the audio data
    :return: the decelerated down audio_data
    """
    # find the averages between 2 near datas

    averages = [[int((data1[0] + data2[0]) / 2),
                 int((data1[1] + data2[1]) / 2)]
                for data1, data2 in zip(audio_data[::1], audio_data[1::1])]

    decelerated = [audio_data[0]]
    for i in range(len(averages)):
        decelerated.append(averages[i])
        decelerated.append(audio_data[i + 1])

    return decelerated


def under_minimum_vol(num):
    """
    checks if the number is under the minimum allowed
    :param num: the number to check
    :return: num if over minimum else MINIMUM
    """
    if num < MINIMUM_VOLUME:
        return MINIMUM_VOLUME
    return num


def over_maximum_vol(num):
    """
    checks if the number is over the maximum allowed
    :param num: the number to check
    :return: num if under the maximum else MAXIMUM
    """
    if num > MAXIMUM_VOLUME:
        return MAXIMUM_VOLUME
    return num


def put_in_range(audio_data):
    """
    puts all audio data received in the range needed
    :param audio_data: the audio data
    :return: None
    """
    for data in audio_data:
        if data[0] < 0:
            data[0] = under_minimum_vol(data[0])
        else:
            data[0] = over_maximum_vol(data[0])

        if data[1] < 0:
            data[1] = under_minimum_vol(data[1])
        else:
            data[1] = over_maximum_vol(data[1])


def increase_volume(audio_data):
    """
    increases the volume of the audio by the constant
    :param audio_data: the audio data
    :return: the increased volume of the audio
    """
    increased = [[int(audio[0] * INCREASE_VOLUME), int(audio[1] *
                                                       INCREASE_VOLUME)]
                 for audio in audio_data]
    # make sure that we are in range
    put_in_range(increased)

    return increased


def decrease_volume(audio_data):
    """
    decreases the given volume by the constant
    :param audio_data: the audio data
    :return: the decreased volume of the data
    """
    decreased = [[int(audio[0] / INCREASE_VOLUME), int(audio[1] /
                                                       INCREASE_VOLUME)]
                 for audio in audio_data]
    # make sure that we are in range
    put_in_range(decreased)

    return decreased


def low_pass_filter(audio_data):
    """
    filters the audio data
    :param audio_data: the audio data
    :return: the filtered audio data
    """
    # first value of the filter
    low_pass = [[int((audio_data[0][0] + audio_data[1][0]) / 2),
                 int((audio_data[0][1] + audio_data[1][1]) / 2)]]

    low_pass = low_pass + ([[int((data1[0] + data2[0] + data3[0]) / 3),
                             int((data1[1] + data2[1] + data3[1]) / 3)]
                            for data1, data2, data3 in zip(audio_data[::1],
                                                           audio_data[1::1],
                                                           audio_data[2::1])])
    low_pass.append([int((audio_data[len(audio_data) - 1][0] +
                          audio_data[len(audio_data) - 2][0]) / 2),
                     int((audio_data[len(audio_data) - 1][1] +
                          audio_data[len(audio_data) - 2][1]) / 2)])

    return low_pass


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
        audio_data = EDIT_MENU[choice](audio_data)
        choice = get_valid_input(EDIT_MENU_MSG, INVALID_CHOICE_ERR_FORMAT,
                                 lambda c: c not in EDIT_MENU)
    exit_menu(frame_rate, audio_data)


def compose_notes(compose_directions):
    """
    Composes a new melody by the instructions given
    :param compose_directions: A list of tuples, each tuple is of the form:
    (NOTE, DURATION)
    :return: A list of WAV audio data
    """
    melody = []
    for note, duration in compose_directions:
        note_data = []
        samples_num = int((duration / 16) * SAMPLE_RATE)
        if note in NOTE_TO_FREQ:
            samples_per_cycle = SAMPLE_RATE / NOTE_TO_FREQ[note]
            for i in range(samples_num):
                sample_value = int(MAXIMUM_VOLUME * math.sin(
                    math.pi * 2 * (i / samples_per_cycle)))
                note_data.append([sample_value, sample_value])
        elif note == QUITE_NOTE:
            note_data = [[0, 0]] * samples_num
        melody += note_data
    return melody


def get_notes(file_location):
    """
    opens file and for each note writes how long to write it
    :param file_location: the location of the file to play
    :return: list of list with each note and how long to play it
    """
    with open(file_location, 'r') as compose_file:
        data = compose_file.read()
        audio_notes = [item for item in re.split(r'\s+', data) if item != '']
    return [[note, int(length)] for note, length in zip(audio_notes[::2], audio_notes[1::2])]


def compose_menu():
    """
    Composes a new WAV file from the user's directions
    :return: None
    """
    composition_file_name = get_valid_input(
        COMPOSE_MENU_MSG,
        INVALID_INPUT_DIRECTIONS_FILE_ERR_FORMAT,
        lambda f: not os.path.isfile(f))
    compose_directions = get_notes(composition_file_name)
    audio_data = compose_notes(compose_directions)
    edit_menu(SAMPLE_RATE, audio_data)


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
    '1': reverse_audio,
    '2': accelerate_audio,
    '3': decelerate_audio,
    '4': increase_volume,
    '5': decrease_volume,
    '6': low_pass_filter,
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
