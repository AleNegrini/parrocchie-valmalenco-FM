import os
import pytest
from parrocchie_valmalenco_fm.orari_config import OrariConfig


class TestOrariConfig:
    filename = "./tmpTest.txt"

    def setup(self):
        f = open(TestOrariConfig.filename, "w+")
        f.write("torre,27/11/2020,07:00,07:40\n")
        f.write("torre,27/11/2020,17:00,22:40\n")
        f.write("caspoggio,28/11/2020,17:00,22:40\n")
        f.close()

    def clear(self):
        os.remove(TestOrariConfig.filename)

    def test_orari_config_ok(self):
        self.setup()

        config = OrariConfig(TestOrariConfig.filename)
        orari = config.read_file()

        self.clear()

    def test_orari_config_fail(self):
        f = open(TestOrariConfig.filename, "w+")
        f.write("torre,27/11/2020,17:00,22:40\n")
        f.write("caspoggio,28/11/2020,17:00,22:40\n")
        f.write("caspoggio,28/11/2020,18:00,23:40\n")
        f.close()

        config = OrariConfig(TestOrariConfig.filename)
        with(pytest.raises(ValueError)):
            orari = config.read_file()

        self.clear()
