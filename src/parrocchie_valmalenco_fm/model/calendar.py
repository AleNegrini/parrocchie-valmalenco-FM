from parrocchie_valmalenco_fm.model.mass import Mass


class Calendar:

    def __init__(self):
        self.mass_list = []

    def check_no_overlap(self):
        """
        Check there are no overlap between mass on the same day
        """
        dict_day_based = {}
        mass_lists = self.mass_list

        for mass in mass_lists:
            (current_start, current_end) = (Mass.hour_to_secs_int(mass.start_hour),
                            Mass.hour_to_secs_int(mass.end_hour))
            if mass.start_day not in dict_day_based:
                dict_day_based[mass.start_day] = [(current_start, current_end)]
            else:
                for tuple_h in dict_day_based[mass.start_day]:
                    if tuple_h[0] < current_start < tuple_h[1]:
                        raise ValueError("Mass in {} at {} is overlapping with "
                                         "another mass.".format(mass.location, mass.start_hour))
                    else:
                        dict_day_based[mass.start_day].append((current_start, current_end))
                        break

    def active_slot(self, date: str, time: str):
        """
        Return active slot for a given date and time
        :param date: Date in format "dd/mm/YYYY"
        :param time: Time in the format "hh:mm"
        :return the location for the active slot
        """
        for mass in self.mass_list:
            if date == mass.start_day and mass.start_hour <= str(time) < mass.end_hour:
                return mass.location

        return None
