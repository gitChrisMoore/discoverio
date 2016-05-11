import re

class IP(object):
    """
    	This class is meant to check and return valid IP address
    	fields.
    """
    @staticmethod
    def _test(ip):
    	try:
    		_match = re.findall(
    			r'([0-9]+(?:\.[0-9]+){3})', ip)
    		return _match[0]
    	except:
    		return None

    @staticmethod
    def _ip_single(ip=None):
    	return IP._test(ip=ip)

    @staticmethod
    def _ip_list(ips=None):
    	filtered_ip_list = []
    	try:
    		for ip in ips:
    			if IP._test(ip=ip):
    				filtered_ip_list.append(ip)
    		return filtered_ip_list
    	except:
    		return None

class Doc(object):
	""" Common Operations that can be performed on a document
		from mongo
	"""

	@staticmethod
	def _check_for_id(Doc):
		try:
			if Doc['_id']:
				return True
		except:
			return False

	@staticmethod
	def _compare_doc_ip(doc_a, doc_b):
		try:
			if IP._ip_single(doc_a['ip_address']) == IP._ip_single(
				doc_b['ip_address']):
				return True
			else:
				return False
		except Exception as e:
			return str(e)

import json
import sys
class Config(object):
	""" Common Operations that can be performed on a document
		from mongo
	"""

	@staticmethod
	def _import_config(file_path):
		try:
			with open(file_path) as data_file:
				result = json.load(data_file)
				return result
		except Exception as e:
			return str(e)

	@staticmethod
	def _load_config(file_path='helpers/config.json'):
		try:
			cfg = {}
			config = Config._import_config(file_path)
			for d in config['db_config']['main']:
				for k,v in d.iteritems():
					cfg[k] = v
			for d in config['db_config']['collection_list']:
				for k,v in d.iteritems():
					cfg[k] = v
			return cfg
		except Exception as e:
			return str(e)

if __name__ == '__main__':
    """ IP Address Validation
    """
    #Test for a valid IP
    if IP._ip_single('1.1.1.1'):
    	print ('IP._ip_single: test : success')
    else:
    	print ('IP._ip_single: test : failed')

    #Test for a valid IP
    if IP._ip_single('a'):
    	print ('IP._ip_single: test : failed')
    else:
    	print ('IP._ip_single: test : success')

    #Test for a valid list of IP
    ip_list = ['1.1.1.1', '2.2.2.2', 'a']
    if len(IP._ip_list(ip_list)) == 2:
    	print ('Multiple Test Passed')

    """ Doc Validation
    """
    valid_Doc = {"test_name": "Valid Doc", "_id": '1'}
    invalid_Doc = {"test_name": "Valid Doc"}
    doc_a = {"ip_address": "1.1.1.1"}
    doc_b = {"ip_address": "1.1.1.1"}
    doc_c = {"ip_address": "3.3.3.3"}
    if Doc._check_for_id(valid_Doc):
    	print Doc._check_for_id(valid_Doc)
    if Doc._check_for_id(invalid_Doc):
    	print Doc._check_for_id(invalid_Doc)
    else:
    	print 'success'

    print Doc._compare_doc_ip(doc_a, doc_b)
    print Doc._compare_doc_ip(doc_a, doc_c)
    print Config._load_config()
