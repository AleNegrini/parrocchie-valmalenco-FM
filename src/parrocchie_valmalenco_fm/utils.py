from datetime import date, datetime


def get_current_date():
    """
    :return: the current date in format %d/%m/%Y
    """
    return date.today().strftime("%d/%m/%Y")


def get_current_time():
    """
    :return: the current time in format %H:%M
    """
    return datetime.now().strftime("%H:%M")


def active_slot(date, time, dictionary):
    for key in dictionary.keys():
        if key[0] == date and key[1] <= str(time) < key[2]:
            return dictionary[key]
    return None
