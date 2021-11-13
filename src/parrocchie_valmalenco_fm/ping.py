import logging
from ping3 import ping


class Ping:

    @staticmethod
    def check_ping(url, timeout=59):
        """
        It checks whether a URL is reachable and returns values accordingly
        Args:
            url: url to test
            timeout: timeout seconds
        Returns:
            It returns a boolean value. True if the URL is reachable, False otherwise.
        """

        response = ping(dest_addr=url, timeout=timeout)
        if response is None:
            logging.info("%s ping failed", url)
            return False
        else:
            logging.info("%s ping successful", url)
            return True
