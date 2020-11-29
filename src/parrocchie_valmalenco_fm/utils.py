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



