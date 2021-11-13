from parrocchie_valmalenco_fm.ping import Ping
from unittest.mock import patch


class TestPing:

    @patch('parrocchie_valmalenco_fm.ping.ping')
    def test_ping_ok(self, mock_ping):
        print(mock_ping)
        mock_ping.return_value = True

        assert Ping.check_ping("dummyurl")

    @patch('parrocchie_valmalenco_fm.ping.ping')
    def test_ping_fail(self, mock_ping):
        mock_ping.return_value = None

        assert not Ping.check_ping("dummyurl")
