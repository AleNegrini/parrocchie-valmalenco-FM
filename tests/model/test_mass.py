from parrocchie_valmalenco_fm.model.mass import Mass


class TestMass:
    calendar = Mass("caspoggio", "27/10/2020", "18:00", "19:00")
    assert Mass.hour_to_secs_int(calendar.start_hour) == 18 * 3600
