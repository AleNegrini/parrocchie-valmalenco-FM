import pytest

from parrocchie_valmalenco_fm.model.calendar import Calendar
from datetime import datetime


class TestCalendar:

    def test_validate_ok(self):
        calendar = Calendar()
        calendar.add_row("caspoggio", "27/10/2020", "18:00", "19:00", calendar.rows)
        calendar.add_row("torre", "27/10/2020", "20:00", "21:00", calendar.rows)
        calendar.add_row("spriana", "27/10/2020", "22:00", "23:00", calendar.rows)
        assert calendar.line_with_errors == 0
        assert calendar.line_ok == 3

    def test_validate_fail(self):
        calendar = Calendar()
        calendar.add_row("caspoggio", "27/10/2020", "18:00", "20:00", calendar.rows)
        calendar.add_row("lanzada", "27/10/2020", "19:00", "21:00", calendar.rows)
        calendar.add_row("spriana", "27/10/2020", "20:00", "21:00", calendar.rows)
        assert calendar.line_with_errors == 2
        assert calendar.line_ok == 1

    def test_active_slot(self):
        calendar = Calendar()
        calendar.add_row("caspoggio", "27/10/2020", "18:00", "20:00", calendar.rows)
        calendar.add_row("torre", "28/10/2020", "19:00", "21:00", calendar.rows)
        assert calendar.line_with_errors == 0
        assert calendar.line_ok == 2
        datetime_format = "%d/%m/%Y %H:%M"
        assert calendar.active_slot(datetime.strptime("27/10/2020 18:30", datetime_format)) == "caspoggio"
        assert calendar.active_slot(datetime.strptime("28/10/2020 19:30", datetime_format)) == "torre"
        assert calendar.active_slot(datetime.strptime("29/10/2020 19:30", datetime_format)) == None

