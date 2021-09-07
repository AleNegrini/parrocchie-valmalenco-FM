
from parrocchie_valmalenco_fm.model.calendar import Calendar


class OrariConfig:
    def __init__(self, path, logging=None, valid_locations=None):
        self.calendar = Calendar(logging, valid_locations)
        self.calendar.read_csv(path)
