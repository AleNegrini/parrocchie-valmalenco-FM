from enum import Enum
from datetime import datetime


class CalendarFieldError(Enum):
    INVALID_INDEX = 1
    EMPTY_FIELD = 2
    INVALID_VALUE = 3


class CalendarField:
    def __init__(self):
        index = -1
        name = "NoName"

    def __base_set_value(self, value):
        if value:
            value = value.strip()
        if value:
            self.value = value
            self.error = None
        else:
            self.value = None
            self.error = CalendarFieldError.EMPTY_FIELD

    def set_value(self, value):
        self.__base_set_value(value)

    def set_value_csv(self, row, index, name):
        self.index = index
        self.name = name
        self.value = None
        self.error = None
        self.valueErrorDetails = None

        n = len(row)
        if n > self.index:
            v = row[self.index]
            self.__base_set_value(v)
        else:
            self.error = CalendarFieldError.INVALID_INDEX

    def is_valid(self):
        return self.error is None


class CalendarLocationField(CalendarField):
    def __init__(self):
        super().__init__()

    def set_value(self, value, valid_values=None):
        super().set_value(value)
        self.__chech_errors(valid_values)

    def set_value_csv(self, row, index, name, valid_values=None):
        super().set_value_csv(row, index, name)
        self.__chech_errors(valid_values)

    def __chech_errors(self, valid_values):
        if super().is_valid():
            if valid_values is not None:
                if self.value not in valid_values:
                    self.error = CalendarFieldError.INVALID_VALUE


class CalendarDateTimeField(CalendarField):
    def __init__(self):
        super().__init__()
        self.dtObject = None

    def set_value(self, value, valid_format):
        super().set_value(value)
        self.__chech_errors(valid_format)

    def set_value_csv(self, row, index, name, valid_format):
        super().set_value_csv(row, index, name)
        self.__chech_errors(valid_format)

    def __chech_errors(self, valid_format):
        if super().is_valid():
            try:
                self.dtObject = datetime.strptime(self.value, valid_format)
                self.error = None
                self.error_details = None
            except ValueError as e:
                self.dtObject = None
                self.error = CalendarFieldError.INVALID_VALUE
                self.error_details = str(e)


class CalendarDateOnlyField(CalendarDateTimeField):
    def __init__(self):
        super().__init__()

    def set_value(self, value, valid_format):
        super().set_value(value, valid_format)
        self.__set_date_object()

    def set_value_csv(self, row, index, name, valid_format):
        super().set_value_csv(row, index, name, valid_format)
        self.__set_date_object()

    def __set_date_object(self):
        if self.dtObject is not None:
            self.date = self.dtObject.date()


class CalendarTimeOnlyField(CalendarDateTimeField):
    def __init__(self):
        super().__init__()

    def set_value(self, value, valid_format):
        super().set_value(value, valid_format)
        self.__set_time_object()

    def set_value_csv(self, row, index, name, valid_format):
        super().set_value_csv(row, index, name, valid_format)
        self.__set_time_object()

    def __set_time_object(self):
        if self.dtObject is not None:
            self.time = self.dtObject.time()
