from parrocchie_valmalenco_fm.model.calendarField import *


class CalendarRowError(Enum):
    NULL_FIELDS_LIST = 1
    FIELD_ERRORS = 2
    INVALID_TIME_INTERVAL = 3
    OVERLAPPED_TIME_INTERVAL = 4


class CalendarRow:

    def __init__ (self):
        self.line_number = -1
        self.location_field = None
        self.start_day_field = None
        self.start_hour_field = None
        self.end_hour_field = None
        self.fields = []
        self.error = None

    def set_fields(self, location, start_day, start_hour, end_hour, other_rows, valid_locations=None):
        self.location_field = CalendarLocationField()
        self.location_field.set_value(location, valid_locations)
        self.fields.append(self.location_field)

        self.start_day_field = CalendarDateOnlyField ()
        self.start_day_field.set_value(start_day, "%d/%m/%Y")
        self.fields.append(self.start_day_field)

        self.start_hour_field = CalendarTimeOnlyField()
        self.start_hour_field.set_value(start_hour, "%H:%M")
        self.fields.append(self.start_hour_field)

        self.end_hour_field = CalendarTimeOnlyField()
        self.end_hour_field.set_value(end_hour, "%H:%M")
        self.fields.append(self.end_hour_field)

        self.__check_errors(other_rows)

    def set_fields_csv(self, line_number, row, other_rows, valid_locations=None):
        self.line_number = line_number

        if row is not None:
            self.location_field = CalendarLocationField()
            self.location_field.set_value_csv(row, 0, "location", valid_locations)
            self.fields.append(self.location_field)

            self.start_day_field = CalendarDateOnlyField()
            self.start_day_field.set_value_csv(row, 1, "start_day", "%d/%m/%Y")
            self.fields.append(self.start_day_field)

            self.start_hour_field = CalendarTimeOnlyField()
            self.start_hour_field.set_value_csv(row, 2, "start_hour", "%H:%M")
            self.fields.append(self.start_hour_field)

            self.end_hour_field = CalendarTimeOnlyField()
            self.end_hour_field.set_value_csv(row, 3, "end_hour", "%H:%M")
            self.fields.append(self.end_hour_field)

            self.__check_errors(other_rows)
        else:
            self.error = CalendarRowError.NULL_FIELDS_LIST

    def __check_errors(self, other_rows):
        fields_are_valid = True
        for field in self.fields:
            fields_are_valid = fields_are_valid and field.is_valid()

        if fields_are_valid:
            if self.start_hour_field.dtObject < self.end_hour_field.dtObject:
                if self.first_overlap(other_rows) is None:
                    self.error = None
                else:
                    self.error = CalendarRowError.OVERLAPPED_TIME_INTERVAL
            else:
                self.error = CalendarRowError.INVALID_TIME_INTERVAL
        else:
            self.error = CalendarRowError.FIELD_ERRORS

    def is_valid(self):
        return self.error is None

    def __str__(self):
        return "Messa {} il giorno {} dalle {} alle {}".format(self.location_field.value, self.start_day_field.value,
                                                               self.start_hour_field.value, self.end_hour_field.value)
    def first_overlap(self, other_rows):
        """
        Return the first row in other_rows whose hour interval overlaps with the current row
        """
        for r in other_rows:
            if self.start_day_field.date == r.start_day_field.date and r.start_hour_field.time <= self.start_hour_field.time <= r.end_hour_field.time:
                return r
        return None