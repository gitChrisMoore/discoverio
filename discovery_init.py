
import sys
import helpers.ssh_child
import helpers.db
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
		self.db = helpers.db.DBWrapper(
			remote_address=self.config['db_config']['remote_address'],
			remote_port=self.config['db_config']['remote_port'],
			db_name=self.config['db_config']['db_name'],
			maxSevSelDelay=self.config['db_config']['maxSevSelDelay'])


	def main(self):
		method_name = 'main'
		log.debug('{0}: starting'.format(method_name))

		print self.config['db_config']['collection_todo']
		# Delete all existing devices in the collections
		result = self.db.delete_single_collection(
			collection_name=self.config['db_config']['collection_todo'])
		log.debug('{0}: result: {1}'.format(method_name, result))
		result = self.db.delete_single_collection(
			collection_name=self.config['db_config']['collection_complete'])
		log.debug('{0}: result: {1}'.format(method_name, result))
		result = self.db.delete_single_collection(
			collection_name=self.config['db_config']['collection_inventory'])
		log.debug('{0}: result: {1}'.format(method_name, result))

		# Add seed devices to the collection
		for device in self.config['db_config']['seed_ips']:
			result = self.db.add_ip_if_not_exist(
				ip=device,
				first_collection=self.config['db_config']['collection_complete'],
				second_collection=self.config['db_config']['collection_todo'])
			log.debug('{0}: result: {1}'.format(method_name, result))


# ================================================================
# MAIN
# ================================================================
if __name__ == '__main__':
    tmprun = DiscoveryInit()
    tmprun.main()
