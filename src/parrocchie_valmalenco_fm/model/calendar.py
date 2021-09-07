from datetime import datetime
from parrocchie_valmalenco_fm.model.calendarRow import CalendarRow, CalendarRowError
import csv

class Calendar:
    def __init__(self, logging=None, valid_locations=None):
        self.logging = logging
        self.valid_locations = valid_locations
        self.rows = []
        self.rows_with_errors = []
        self.current_line = 1
        self.line_ok = 0
        self.line_with_errors = 0
        self.processed_lines = 0

    def __log(self, message):
        if self.logging is not None:
            self.logging.info(message)
        else:
            print(message)

    def add_row(self, location, start_day, start_hour, end_hour, other_rows, valid_locations=None):
        cr = CalendarRow()
        cr.set_fields(location, start_day, start_hour, end_hour, other_rows, valid_locations)
        self.__try_append_row(cr)

    def add_row_csv(self, csv_row):
        cr = CalendarRow()
        cr.set_fields_csv(self.current_line, csv_row, self.rows, self.valid_locations)
        self.__try_append_row(cr)

    def __try_append_row(self, cr):
        if cr.is_valid():
            self.line_ok += 1
            self.rows.append(cr)
        else:
            self.line_with_errors += 1
            self.rows_with_errors.append(cr)
            self.__log("***** Error: {} at line {} *****".format(cr.error, self.current_line))
            if cr.error == CalendarRowError.FIELD_ERRORS:
                for field in cr.fields:
                    if field.error is not None:
                        self.__log(
                            "     ***** Field error (field='{}', index={}, value='{}'): {} *****".format(
                                field.name, field.index, field.value, field.error))
                        if field.valueErrorDetails is not None:
                            self.__log(
                                "          ***** Field error details: {} *****".format(field.error_details))
        self.current_line += 1

    def read_csv(self, path):
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            try:
                for csv_row in csv_reader:
                    self.add_row_csv(csv_row)
            except csv.Error as e1:
                error_message = "csv.Error (riga: {}, errore: {})".format(self.current_line, str(e1))
                self.__log(error_message)

        self.processed_lines = self.line_ok + self.line_with_errors
        self.__log("Messe inserite correttamente: {}/{}".format(self.line_ok, self.processed_lines))
        if self.line_with_errors > 0:
            self.__log("***** Errori nell'inserimento delle messe: {}/{} *****".format(self.line_with_errors,
                                                                                       self.processed_lines))
        else:
            self.__log("Nessun errore nell'inserimento delle messe")

    def active_slot(self, now=None):
        """
        Return active slot for a given date and time
        :return the location for the active slot
        """
        if now is None:
            now = datetime.now()
        d = now.date()
        t = now.time()

        for r in self.rows:
            if d == r.start_day_field.date and r.start_hour_field.time <= t < r.end_hour_field.time:
                return r.location_field.value
        return None