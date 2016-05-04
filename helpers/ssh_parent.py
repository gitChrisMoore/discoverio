import time
import ssh
import sys
import re
import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)

class SSHWrapper(object):
	""" The object of this class is to provide a wrapper around the paramiko
		package.  There are two main pieces two the package, the transport
		and the channel.  Once the channel is created, if it is a cisco device
		it will disable the paging from interfering with the output
	"""
	def __init__(self,host=None,un=None,pw=None,port=22):
		self.pw = pw
		self.ssh_channel = ssh.SSHBase(host=host,un=un,pw=pw)
		self.ssh_session = self.ssh_channel.create_channel()
		self.ssh_client = self.ssh_session.invoke_shell()
		self.check_enable()

	def main(self,disable_paging=True,command=None):
		method_name = 'main'
		log.debug('{0}: starting'.format(method_name))
		try:
			if disable_paging:
				self.ssh_channel.disable_paging(session=self.ssh_client)
			result = self.ssh_channel.send_command(session=self.ssh_client,
				command=command)
			log.debug('{0}:success: ran command: {1}'.format(
				method_name,result))
			return result
		except Exception as e:
			log.error('{0}:exception:'.format(method_name))
			log.error('{0}:error: {1}'.format(method_name, e))


	def check_enable(self):
		method_name = 'check_enable'
		log.debug('{0}:start:'.format(method_name))
		#Validate that the connection to the database has been made
		try:
			result = self.ssh_channel.send_command(session=self.ssh_client,
				command="en\n")
			if "password:" in result:
				command_string = str(self.pw)+"\n"
				result = self.ssh_channel.send_command(
					session=self.ssh_client,command=command_string)
				time.sleep(1)
				log.debug('{0}:success: ran enable ' \
					'command on destination'.format(method_name))
				log.debug('{0}:result: {1})'.format(method_name, result))
		except Exception as e:
			log.error('{0}:exception:'.format(method_name))
			log.error('{0}:error: {1}'.format(method_name, e))