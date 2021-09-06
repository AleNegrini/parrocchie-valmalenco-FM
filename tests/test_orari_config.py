import csv
import os
import pytest
from parrocchie_valmalenco_fm.orari_config import OrariConfig
from parrocchie_valmalenco_fm.config import Config
from parrocchie_valmalenco_fm.camera_config import CameraConfig

ORARI_FILE = 'orari.csv'
RELAY_CONFIG_FILE = 'config-relay.ini'
CAMERA_CONFIG_FILE = 'config.ini'


class TestOrariConfig:
    filename = "./tmpTest.txt"

    def clear(self):
        os.remove(TestOrariConfig.filename)

    def test_orari_config_ok(self):
        f = open(TestOrariConfig.filename, "w+")
        f.write("torre,27/11/2020,07:00,07:40\n")
        f.write("torre,27/11/2020,17:00,22:40\n")
        f.write("caspoggio,28/11/2020,17:00,22:40\n")
        f.close()

        valid_locations = ["torre", "caspoggio"]
        config = OrariConfig(TestOrariConfig.filename, None, valid_locations)
        orari = config.read_file()

        assert(config.line_number, 3)
        assert(config.line_ok, 3)
        assert(config.line_with_errors, 0)

        self.clear()

    def test_orari_config_location_error(self):
        f = open(TestOrariConfig.filename, "w+")
        f.write("torre,27/11/2020,07:00,07:40\n")
        f.write("torre,27/11/2020,17:00,22:40\n")
        f.write("casp oggio,28/11/2020,17:00,22:40\n")
        f.close()

        valid_locations = ["torre", "caspoggio"]
        config = OrariConfig(TestOrariConfig.filename, None, valid_locations)
        orari = config.read_file()

        assert(config.line_number, 3)
        assert(config.line_ok, 2)
        assert(config.line_with_errors, 1)

        self.clear()

    def test_orari_config_fail(self):
        f = open(TestOrariConfig.filename, "w+")
        f.write("torre,27/11/2020,17:00,22:40\n")
        f.write("caspoggio,28/11/2020,17:00,22:40\n")
        f.write("caspoggio,28/11/2020,18:00,23:40\n")
        f.close()

        config = OrariConfig(TestOrariConfig.filename)
        with(pytest.raises(ValueError)):  # fixme: this exception is now catched
            orari = config.read_file()

        self.clear()

    def test_orari_csv_error(self):
        f = open(TestOrariConfig.filename, "w+")
        f.write("torre,27/11/2020231,17:00,22:40\n")
        f.write("\n")
        f.close()

        config = OrariConfig(TestOrariConfig.filename)
        with(pytest.raises(csv.Error)): # fixme: this exception does not occur
            orari = config.read_file()

        self.clear()

    def test_orari_index_error(self):
        f = open(TestOrariConfig.filename, "w+")
        f.write("torre,27/11/2020,17:00,22:40\n")
        f.write("caspoggio,28/11/2020,17:")
        f.close()

        config = OrariConfig(TestOrariConfig.filename)
        with(pytest.raises(IndexError)): # fixme: this exception is now catched
            orari = config.read_file()

        self.clear()
