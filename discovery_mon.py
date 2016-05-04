import sys
import helpers.db2
import helpers.load_config
import time
import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)

class DiscoveryMon(object):
	""" This loops through the available collections from the configuraiton
		file and every 10 seconds does a count on the configured collections
	"""

	def __init__(self):
		self.config = helpers.load_config.load_config(self)
		# Create the DB object
		self.db = helpers.db2.DBWrapper()
		self.db.start_conn()


	def main(self):
		method_name = 'main'

		while True:
			result_array = []
			for d in self.db.cfg['collection_list']:
				for k,v in d.iteritems():
					result = self.db.count_collection(collection=v)
					tmp_obj = {v : result}
					result_array.append(tmp_obj)
			log.info('\n\nresult:collection_todo: \n{0}'.format(
				result_array))
			time.sleep(10)

# ================================================================
# MAIN
# ================================================================
if __name__ == '__main__':
    tmprun = DiscoveryMon()
    tmprun.main()
