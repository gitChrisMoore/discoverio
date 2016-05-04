#ssh_helper.py
import paramiko
import time
import sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)

class SSHBase(object):
	""" The object of this class is to provide a wrapper around the paramiko
		package.  There are two main pieces two the package, the transport
		and the channel.  Once the channel is created, if it is a cisco device
		it will disable the paging from interfering with the output
	"""
	def __init__(self,host=None,un=None,pw=None,port=22):
		self.host = host
		self.un = un
		self.pw = pw
		self.port = port
		self.execute_command = ''

	def main(self):
		method_name = 'main'
		log.debug('{0}: starting'.format(method_name))

	def create_channel(self):
		method_name = 'create_channel'
		log.debug('{0}:starting:'.format(method_name))
		log.debug('{0}:try:{1} {2} {3}'.format(
			method_name,self.host, self.port, self.un))
		#Try and connect to the remote host
		ssh_transport = paramiko.SSHClient()
		ssh_transport.set_missing_host_key_policy(
			paramiko.AutoAddPolicy())
		try:
			ssh_transport.connect(hostname=self.host, 
				port=self.port, password=self.pw, username=self.un)
			log.debug('{0}:success: {1} {2} {3}'.format(
				method_name,self.host, self.port, self.un))
			log.debug('{0}:result: {1})'.format(method_name,ssh_transport))
			return ssh_transport
		except Exception as e:
			log.error('{0}:exception: {1} {2} {3}'.format(
				method_name,self.host, self.port, self.un))
			log.error('{0}:error: {1}'.format(method_name, e))

	def disable_paging(self,session):
		method_name = 'disable_paging'
		log.debug('{0}:starting:'.format(method_name))
		session.send("terminal length 0\n")
		time.sleep(.5)
		output = session.recv(1000)
		return output


	def send_command(self,session,command,timeout=5,bufsize=65536,
						output_idle_counter_max=3):
		method_name = 'send_command'
		log.debug('{0}:starting:'.format(method_name))
		log.debug('{0}:try:{1} {2} {3}'.format(
			method_name,command, bufsize, output_idle_counter_max))

		output_place_holder = 'a'
		output_idle_counter = 0
		output = ''
		try:
			time.sleep(.1)
			session.send(command)
			log.debug('{0}:command:{1}'.format(method_name,command))
			time.sleep(.35)
			while True:
				log.debug('{0}: Starting while True'.format(method_name))
				if session.recv_ready():
					data = session.recv(bufsize)
					output += data
				if len(output) == len(output_place_holder):
					output_idle_counter += 1
				output_place_holder = output
				if output_idle_counter == output_idle_counter_max:
					log.debug('{0}: Break while true'.format(method_name))
					return output
					break
				time.sleep(0.200)

		except Exception as e:
			log.error('{0}:exception: {1} {2} {3}'.format(
				method_name,self.host, self.port, self.un))
			log.error('{0}:error: {1}'.format(method_name, e))