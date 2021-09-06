from enum import Enum
from datetime import datetime


class CalendarFieldError(Enum):
    INVALID_INDEX = 1
    EMPTY_FIELD = 2
    INVALID_VALUE = 3


class CalendarField:
    def __init__(self, row, index, name):
        self.row = row
        self.index = index
        self.name = name
        self.value = None
        self.error = None
        self.valueErrorDetails = None

        n = len(self.row)
        if n > self.index:
            v = self.row[self.index]
            if v:
                v = v.strip()
            if v:
                self.value = v
            else:
                self.error = CalendarFieldError.EMPTY_FIELD
        else:
            self.error = CalendarFieldError.INVALID_INDEX

    def is_valid(self):
        return self.error is None


class CalendarLocationField(CalendarField):
    def __init__(self, row, index, name, valid_values=None):
        CalendarField.__init__(self, row, index, name)
        self.valid_values = valid_values

    def is_valid(self):
        if super().is_valid():
            if self.valid_values is None:
                self.error = None
                return True
            if self.value in self.valid_values:
                self.error = None
                return True
            else:
                self.error = CalendarFieldError.INVALID_VALUE
                return False
        return False


class CalendarDateTimeField(CalendarField):
    def __init__(self, row, index, name, valid_format):
        CalendarField.__init__(self, row, index, name)
        self.valid_format = valid_format
        self.dtObject = None

    def is_valid(self):
        if super().is_valid():
            try:
                self.dtObject = datetime.strptime(self.value, self.valid_format)
                self.valueErrorDetails = None
                return True
            except ValueError as e:
                self.valueErrorDetails = e
                return False

        return False
