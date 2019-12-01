import math

INCREASE_VOLUME = 1.2
DECREASE_VOLUME = 1.2
MINIMUM_VOLUME = -32768
MAXIMUM_VOLUME = 32767
SAMPLE_RATE = 2000
NUM_TO_SECONDS = 1/16
NOTE_TO_FREQ = {
    'A': 440,
    'B': 494,
    'C': 523,
    'D': 587,
    'E': 659,
    'F': 698,
    'G': 784
}


def reverse_audio(audio_data):
    """
    reverses the given audio data
    :param audio_data: the audio data
    :return: the reversed audio_data
    """
    return audio_data.reverse()


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
    low_pass = [[int((audio_data[0][0]) + (audio_data[1][0]) / 2),
                 int((audio_data[0][1]) + (audio_data[1][1]) / 2)]]
    low_pass.append([[int((data1[0] + data2[0] + data3[0]) / 3),
                      int((data1[1] + data2[1] + data3[1]) / 3)]
                     for data1, data2, data3 in zip(audio_data[::1],
                                                    audio_data[1::1],
                                                    audio_data[2::1])])
    low_pass.append([int((audio_data[len(audio_data) - 1][0] +
                     audio_data[len(audio_data) - 2][0]) / 2),
                     int((audio_data[len(audio_data) - 1][1] +
                     audio_data[len(audio_data) - 2][1]) / 2)])

    return low_pass


def get_notes(file_location):
    """
    opens file and for each note writes how long to write it
    :param file_location: the location of the file to play
    :return: list of list with each note and how long to play it
    """
    ############FIX######################3
    with open(file_location, 'r') as file:
        line = file.readline()
        audio_notes = line.split(' ')

    return [[note, length] for note, length in zip(audio_notes[::2], audio_notes[1::2])]
