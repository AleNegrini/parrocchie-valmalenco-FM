class Mass:
    def __init__(self, location, start_day, start_hour, end_hour):
        self.location = location
        self.start_day = start_day
        self.start_hour = start_hour
        self.end_hour = end_hour

    @staticmethod
    def hour_to_secs_int(str_hour: str):
        (h, m) = str_hour.split(':')
        return int(h) * 3600 + int(m) * 60
