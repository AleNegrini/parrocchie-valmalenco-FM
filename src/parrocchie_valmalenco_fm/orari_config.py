import csv

from parrocchie_valmalenco_fm.model.mass import Mass
from parrocchie_valmalenco_fm.model.calendar import Calendar


class OrariConfig:

    def __init__(self, path):
        self.path = path
        self.calendar = Calendar()

    def read_file(self):
        """
        Reading and parsing the input file
        :param path: file path
        :return: dictionary
        """

        with open(self.path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                calendar_obj = Mass(row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip())
                self.calendar.mass_list.append(calendar_obj)
                line_count += 1

        self.calendar.check_no_overlap()
        print("Calendar file is valid.")

        return self.calendar
