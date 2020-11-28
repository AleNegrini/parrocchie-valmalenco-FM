import os
import pytest
from parrocchie_valmalenco_fm.config import Config


class TestConfig:

    def test_config_check_exists(self):
        filename = "tmpTest.txt"

        config = Config("./")
        f = open(filename, "w+")

        ret_dict = config.config_check([filename])
        os.remove(filename)
        assert ret_dict[filename]

    def test_config_check_fail(self):

        with pytest.raises(SystemExit):
            config = Config("./")
            config.config_check(["invalid_file"])
