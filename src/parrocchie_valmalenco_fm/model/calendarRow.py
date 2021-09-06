from parrocchie_valmalenco_fm.model.calendarField import *
class CalendarRowError(Enum):
    NULL_FIELDS_LIST = 1
    FIELD_ERRORS = 2
    INVALID_TIME_INTERVAL = 3


class CalendarRow:
    def __init__(self, line_number, row, valid_locations=None):
        self.line_number = line_number
        self.row = row
        self.valid_locations = valid_locations
        self.error = None
        self.fieldList = []
        self.location = None
        self.startDate = None
        self.startHour = None
        self.endHour = None

        if self.row is not None:
            self.location = CalendarLocationField(self.row, 0, "location", self.valid_locations)
            self.fieldList.append(self.location)
            self.startDate = CalendarDateTimeField(self.row, 1, "start_day", "%d/%m/%Y")
            self.fieldList.append(self.startDate)
            self.startHour = CalendarDateTimeField(self.row, 2, "start_hour", "%H:%M")
            self.fieldList.append(self.startHour)
            self.endHour = CalendarDateTimeField(self.row, 3, "end_hour", "%H:%M")
            self.fieldList.append(self.endHour)

            fields_are_valid = True
            for field in self.fieldList:
                fields_are_valid = fields_are_valid and field.is_valid()

            if fields_are_valid:
                if self.startHour.dtObject < self.endHour.dtObject:
                    self.error = None
                else:
                    self.error = CalendarRowError.INVALID_TIME_INTERVAL
            else:
                self.error = CalendarRowError.FIELD_ERRORS
        else:
            self.error = CalendarRowError.NULL_FIELDS_LIST
