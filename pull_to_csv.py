from dns import resolver,reversename
import helpers.db2
import logging
import sys
import csv

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)





class BuildContainers(object):

	def __init__(self):
		self.db2 = helpers.db2.DB()

	def main(self):
		cursor = self.db2.find_all(col='discovery_cdp')
		f = csv.writer(open("/tmp/test.csv", "wb+"))
		f.writerow(["neighbor_platform", "dns_name", "neighbor_remote_port", "neighbor_capabilities", "mac_address", "ip_address"])
		counter = 0

		while counter < 10:
			for i in cursor:
				doc = {
				'neighbor_platform': '',
				'dns_name': '',
				'neighbor_remote_port': '',
				'neighbor_capabilities': '',
				'mac_address': '',
				'ip_address': '',
				}
				z = self.merge_two_dicts(doc, i)
				f.writerow([z['neighbor_platform'],
					z['dns_name'],
					z['neighbor_remote_port'],
					z['neighbor_capabilities'],
					z['mac_address'],
					z['ip_address']])


	def merge_two_dicts(self,x, y):
	    '''Given two dicts, merge them into a new dict as a shallow copy.'''
	    z = x.copy()
	    z.update(y)
	    return z


if __name__ == "__main__":
    client = BuildContainers()
    client.main()