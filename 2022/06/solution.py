def scan_signal(signal, marker_length):

    in_range = True
    for index in range(len(signal)):

        # Build the candidate marker
        candidate_marker = []
        for marker_position in range(marker_length):
            if index + marker_length <= len(signal):
                candidate_marker += signal[index + marker_position]
            else:
                in_range = False

        # Stop if the end of the signal has been reached
        if not in_range:
            break

        # Check if all characters are unique
        if len(set(candidate_marker)) == marker_length:
            print("First valid marker: {}\nCharacters processed: {}".format(candidate_marker, index + marker_length))
            break


with open('2022/06/input.txt') as file:
    signal = file.read()

scan_signal(signal, marker_length=4)  # Part 1
scan_signal(signal, marker_length=14)  # Part 2
