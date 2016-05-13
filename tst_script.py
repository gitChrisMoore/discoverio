from dns import resolver,reversename
import helpers.db2
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)





class BuildContainers(object):

	def __init__(self):
		self.db2 = helpers.db2.DB()

	def main(self):
		cursor = self.db2.find_all(col='discovery_cdp')

		counter = 0

		while counter < 10:
			for i in cursor:
				addr = ''
				dns_name = ''
				try:
					addr=reversename.from_address(i['ip_address'])
					dns_name = str(resolver.query(addr,"PTR")[0])				
					doc = {'ip_address': i['ip_address'], 'dns_name': dns_name}
					print self._add_dns(item=doc)
				except Exception as e:
					print str(e)

				counter += 1

	def _add_dns(self, item):
		log.debug('starting: _add_dns')
		try:
			print self.db2.upsert_dns(col='discovery_cdp', doc=item)
		except Exception as e:
			log.error('error: {0}'.format(str(e)))


if __name__ == "__main__":
    client = BuildContainers()
    client.main()