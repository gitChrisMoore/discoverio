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
		self.cfg = helpers.cmn_tool.Config._load_config()
		# Create the DB object
		self.db = helpers.db2.DB()

	def main(self):
		while True:
			result_array = []
			for d in self.cfg['db_config']['collection_list']:
				for k,v in d.iteritems():
					result = self.db.count(col=v)
					tmp_obj = {v : result}
					result_array.append(tmp_obj)
			log.info('\n\nresults: {0}'.format(result_array))
			time.sleep(10)

# ================================================================
# MAIN
# ================================================================
if __name__ == '__main__':
    tmprun = DiscoveryMon()
    tmprun.main()
