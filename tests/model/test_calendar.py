import pytest

from parrocchie_valmalenco_fm.model.calendar import Calendar
from parrocchie_valmalenco_fm.model.mass import Mass


class TestCalendar:


    def test_validate_ok(self):
        calendar = Calendar()

        mass1 = Mass("caspoggio", "27/10/2020", "18:00", "19:00")
        calendar.mass_list.append(mass1)

        mass2 = Mass("torre", "27/10/2020", "20:00", "21:00")
        calendar.mass_list.append(mass2)

        mass3 = Mass("spriana", "27/10/2020", "20:00", "21:00")
        calendar.mass_list.append(mass3)

        calendar.check_no_overlap()

    def test_validate_fail(self):
        calendar = Calendar()

        mass1 = Mass("caspoggio", "27/10/2020", "18:00", "20:00")
        calendar.mass_list.append(mass1)

        mass2 = Mass("lanzada", "27/10/2020", "19:00", "21:00")
        calendar.mass_list.append(mass2)

        mass3 = Mass("spriana", "27/10/2020", "20:00", "21:00")
        calendar.mass_list.append(mass3)

        with(pytest.raises(ValueError)):
            calendar.check_no_overlap()


    def test_active_slot_empty(self):
        calendar = Calendar()

        assert calendar.active_slot("29/10/2020", "19:30") == None
        assert calendar.active_slot("30/10/2020", "19:30") == None

    def test_active_slot(self):
        calendar = Calendar()

        mass1 = Mass("caspoggio", "27/10/2020", "18:00", "20:00")
        calendar.mass_list.append(mass1)

        mass2 = Mass("torre", "28/10/2020", "19:00", "21:00")
        calendar.mass_list.append(mass2)

        assert calendar.active_slot("27/10/2020", "18:30") == "caspoggio"
        assert calendar.active_slot("28/10/2020", "19:30") == "torre"
        assert calendar.active_slot("29/10/2020", "19:30") == None

