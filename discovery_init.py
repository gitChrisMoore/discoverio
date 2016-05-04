
import sys
import helpers.ssh_child
import helpers.db
import helpers.db2
import helpers.load_config
import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)

class DiscoveryInit(object):
	""" This provides a wrapper around the MongoClient package, and also 
	allows for some default values to be added.
	"""

	def __init__(self):
		self.config = helpers.load_config.load_config(self)
		# Create the DB object
		self.db = helpers.db2.DBWrapper()
		self.db.start_conn()


	def main(self):
		method_name = 'main'
		log.debug('{0}: starting'.format(method_name))

		# Delete all existing devices in the collections
		for d in self.db.cfg['collection_list']:
			for k,v in d.iteritems():
				result = self.db.delete_single_collection(collection_name=v)
		
		
		# Add seed devices to the collection
		for device in self.config['db_config']['seed_ips']:
			result = self.db.add_ip_if_not_exist(
				ip=device,
				first_collection=self.db.cfg['complete'],
				second_collection=self.db.cfg['todo'])
			log.debug('{0}: result: {1}'.format(method_name, result))


# ================================================================
# MAIN
# ================================================================
if __name__ == '__main__':
    tmprun = DiscoveryInit()
    tmprun.main()
