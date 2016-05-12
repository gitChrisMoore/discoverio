import sys
import helpers.db2
import helpers.cmn_tool
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
		self.cfg = helpers.cmn_tool.Config._load_config()
		# Create the DB object
		self.db = helpers.db2.DB()

	def main(self):

		for d in self.cfg['db_config']['collection_list']:
			for k,v in d.iteritems():
				result = self.db.find_all(col=v)
				for i in result:
					with open('/tmp/' + v + '.txt', 'a') as the_file:
						the_file.write(str(i))
						the_file.write('\n')


# ================================================================
# MAIN
# ================================================================
if __name__ == '__main__':
    tmprun = DiscoveryMon()
    tmprun.main()
