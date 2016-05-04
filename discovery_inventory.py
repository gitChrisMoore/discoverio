import sys
import helpers.db2
import helpers.load_config
import time
import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)

class DiscoveryMon(object):
	""" This provides a wrapper around the MongoClient package, and also 
	allows for some default values to be added.
	"""

	def __init__(self):
		self.config = helpers.load_config.load_config(self)
		# Create the DB object
		self.db = helpers.db2.DBWrapper()
		self.db.start_conn()

	def main(self):
		while True:
			result_inventory_collection = self.db.find_all(
				collection=self.config['db_config']['collection_inventory'])
			for document in result_inventory_collection:
				log.debug('\n\nresult:find_all: \n{0}'.format(
					document))
				print document
			time.sleep(60)

# ================================================================
# MAIN
# ================================================================
if __name__ == '__main__':
    tmprun = DiscoveryMon()
    tmprun.main()
