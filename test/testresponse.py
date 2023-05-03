'''
Check opennem.org.au api for successful response

To carry out test: python -m unittest test.testresponse -v from ./

Author: Oliver Gruber
2/5/2023
'''

import unittest
from requesthandling import send_request
from originenergyapi import show_origin_energy_power_generation_sites


class TestSuccessfulResponse(unittest.TestCase):

	def setUp(self):
		self.origin_energy_power_generation_sites = show_origin_energy_power_generation_sites()

	def test_successful_response_code(self):
		''' check power station api codes in origin_energy_power_generation_sites are valid '''

		for station_code in range(len(self.origin_energy_power_generation_sites )):
			self.response = send_request('https://api.opennem.org.au/stats/energy/station/nem/' + \
									self.origin_energy_power_generation_sites [station_code]['apicode'])
			print(self.response)
			self.assertEqual(self.response.status_code, 200)

	def test_fail_response_code(self):
		''' check power station api codes in origin_energy_power_generation_sites are valid '''

		''' deliberate fictional station code '''
		self.response = send_request('https://api.opennem.org.au/stats/energy/station/nem/FOO')
		print(self.response)
		self.assertNotEqual(self.response.status_code, 200)


if __name__ == '__main__':
	unittest.main()