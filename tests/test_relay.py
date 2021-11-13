import requests

from parrocchie_valmalenco_fm.relay import Relay
from unittest import mock
from unittest.mock import patch

class TestRelay:

	def setup(self):
		self.relay_ip = '192.168.1.199'
		self.relay_block_ip = '192.168.1.200'
		self.test_relay = Relay(self.relay_ip, self.relay_block_ip)

	def test_attributes(self):
		assert self.test_relay.relay_ip == self.relay_ip
		assert self.test_relay.relay_block_ip == self.relay_block_ip

	# This method will be used by the mock to replace requests.get
	def __mocked_requests_get(self, url):
		r = requests.Response()
		r.status_code = 200
		r.json = "Success"
		return r

	def __mocked_requests_fail_3000_01(self, url):

		if url.contains("3000/01"):
			raise Exception()

		r = requests.Response()
		r.status_code = 200
		r.json = "Success"
		return r

	def __mocked_requests_post(self):
		r = requests.Response()
		r.status_code = 200

		def json_func():
			return "Success"

		r.json = json_func
		return r

	@patch('time.sleep', return_value=None)
	@patch.object(requests, 'get')
	@patch.object(requests, 'post')
	def test_trigger_start_success(self, request_post, request_get, sleep_mock):
		request_get.side_effect = self.__mocked_requests_get
		request_post.return_value = self.__mocked_requests_post()

		self.test_relay.trigger('start')
		assert True  # no exceptions

	@patch('time.sleep', return_value=None)
	@patch.object(requests, 'get')
	@patch.object(requests, 'post')
	def test_trigger_start_fail_3000_01(self, request_post, request_get, sleep_mock):
		request_get.side_effect = self.__mocked_requests_fail_3000_01
		request_post.return_value = self.__mocked_requests_post()

		self.test_relay.trigger('start')
		assert True  # no exceptions