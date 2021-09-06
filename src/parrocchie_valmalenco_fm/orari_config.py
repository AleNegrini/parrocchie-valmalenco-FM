import csv
import sys

from parrocchie_valmalenco_fm.model.mass import Mass
from parrocchie_valmalenco_fm.model.calendar import Calendar
from parrocchie_valmalenco_fm.model.calendarRow import CalendarRow, CalendarRowError


class OrariConfig:

    def __init__(self, path, logging=None, valid_locations=None):
        self.path = path
        self.calendar = Calendar()
        self.logging = logging
        self.valid_locations = valid_locations

        self.line_number = 0
        self.line_ok = 0
        self.line_with_errors = 0

    def __log(self, message):
        if self.logging is not None:
            self.logging.info(message)
        else:
            print(message)

    def read_file(self):
        """
        Reading and parsing the input file
        :return: dictionary
        """

        self.line_number = 0
        self.line_ok = 0
        self.line_with_errors = 0

        self.calendar.mass_list = []
        with open(self.path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            try:
                self.__log("--------> START read file {} (after try)".format(self.path))
                for row in csv_reader:
                    cr = CalendarRow(self.line_number+1, row, self.valid_locations)
                    self.__log("--------> read line = {}".format(self.line_number+1))
                    if cr.error is None:
                        self.line_ok += 1
                        self.__log("self.line_ok = {}".format(self.line_ok))
                        mass = Mass(cr.location.value, cr.startDate.value, cr.startHour.value, cr.endHour.value)
                        self.calendar.mass_list.append(mass)
                        self.__log("{} aggiunta correttamente".format(mass))
                    else:
                        self.line_with_errors += 1
                        self.__log("***** Error: {} at line {}: *****".format(cr.error, self.line_number))
                        if cr.error == CalendarRowError.FIELD_ERRORS:
                            for field in cr.fieldList:
                                if field.error is not None:
                                    self.__log("***** Error in field '{}' (index={}, value='{}'): {} *****".format(field.name, field.index, field.value, field.error))
                                    if field.valueErrorDetails is not None:
                                        self.__log("***** Error details: {} *****".format(field.valueErrorDetails))
                    self.line_number += 1
                self.__log("--------> END read file {} (after try)".format(self.path))
            except csv.Error as e1:
                error_message = "csv.Error (riga: {}, errore: {})".format(self.line_number+1, e1)
                self.__log(error_message)

        try:
            self.__log("qui 1")
            self.calendar.check_no_overlap()  # fixme non entra più qui... boh
            self.__log("qui 2")
        except ValueError:
            self.__log("Value error")

        self.__log("Messe inserite correttamente: {}/{}".format(self.line_ok, self.line_number))
        if self.line_with_errors > 0:
            self.__log("***** Errori nell'inserimento delle messe: {}/{} *****".format(self.line_with_errors,
                                                                                       self.line_number))
        else:
            self.__log("Nessun errore nell'inserimento delle messe")

        self.__log("qui 3")
        return self.calendar
