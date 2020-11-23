import csv


def read_file(path):
    """
    Reading and parsing the input file
    :param path: file path
    :return: dictionary
    """

    calendar = {}

    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            calendar[row[1].strip(), row[2].strip(), row[3].strip()] = row[0].strip()
            line_count += 1

    return calendar
