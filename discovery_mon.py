import sys
import helpers.db
import helpers.load_config
import time
import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)

class DiscoveryMon(object):
	""" This provides a wrapper around the MongoClient package, and also 
	allows for some default values to be added.
	"""

	def __init__(self):
		self.config = helpers.load_config.load_config(self)
		# Create the DB object
		self.db = helpers.db.DBWrapper(
			remote_address=self.config['db_config']['remote_address'],
			remote_port=self.config['db_config']['remote_port'],
			db_name=self.config['db_config']['db_name'],
			maxSevSelDelay=self.config['db_config']['maxSevSelDelay'],)

	def main(self):
		method_name = 'main'

		while True:
			result_collection_todo = self.db.count_collection(
				collection=self.config['db_config']['collection_todo'])
			result_collection_complete = self.db.count_collection(
				collection=self.config['db_config']['collection_complete'])
			result_inventory_collection = self.db.count_collection(
				collection=self.config['db_config']['collection_inventory'])
		
			log.debug('\n\nresult:collection_todo: \n{0}'.format(
				result_collection_todo))
			log.debug('\n\nresult:collection_complete: \n{0}'.format(
				result_collection_complete))
			log.debug('\n\nresult:inventory_collection: \n{0}'.format(
				result_inventory_collection))
			time.sleep(10)

# ================================================================
# MAIN
# ================================================================
if __name__ == '__main__':
    tmprun = DiscoveryMon()
    tmprun.main()
