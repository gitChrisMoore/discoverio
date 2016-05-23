import logging
import sys
import helpers.load_config
import helpers.ssh_child
import helpers.db2
import time
import lib.mapping
import lib.show_ip_route
import lib.show_ip_vrf
import helpers.cmn_tool

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)


class BuildContainers(object):
    """ This provides a wrapper around the MongoClient package, and also
    allows for some default values to be added.
    """

    def __init__(self):
        self.cfg = helpers.cmn_tool.Config._load_config()
        self.db2 = helpers.db2.DB()
        self.director = lib.cmd_director.Director()
        self.stats = {}
        self.vrf = ['default']
        self.ip_discovered_list = []
        self.ip_owned_list = []
        self.filtered_owned_ip_list = []
        self.list_complete = []
        self.list_todo = []
        self.new_device = None

    def main(self):
        # standard start config: start
        self.abs_start(method_name='main')
        # standard start config: end

        while self.db2.todo_count() > 0:
            self.new_device = self.db2.todo_get_doc()
            log.info('starting with new device: {0}'.format(self.new_device))

            self.get_function_list()

            try:
                self.start_ssh_session()

                self.check_for_vrf()

                for vrf in self.vrf:
                    self.loop_show_ip_route(vrf_name=vrf)

                self.main_loop()

                self._add_list_to_cdp()
                self._add_loop_of_lists()
                self._add_list_to_todo()
                self._add_list_to_complete()
                self._add_arp()
                # standard start config: start
                self.abs_end(method_name='main')
                # standard start config: end
                self._add_inventory()
            except Exception as e:
                log.error('error: {0}'.format(str(e)))

    def _build_todo_obj(self, ip):
        return {'ip_address': ip}

    def _dict_to_ip_list(self, device_list):
        log.debug('starting: _dict_to_ip_list')
        tmp_list = []
        for ele in device_list:
            if isinstance(ele,dict):
                for key, value in ele.iteritems():
                    if helpers.cmn_tool.IP._ip_single(value):
                        tmp_list.append(value)
        return tmp_list

    def _list_tp_ip(self, device_list):
        log.debug('starting: _list_tp_ip')
        tmp_list = []
        for ele in device_list:
            if helpers.cmn_tool.IP._ip_single(ele):
                tmp_list.append(ele)
        return tmp_list


    def _add_loop_of_lists(self):
        log.debug('starting: _add_loop_of_lists')

        self.list_complete = []
        self.list_todo = []

        self.list_complete = self.list_complete + self._dict_to_ip_list(self.ip_interface)
        #
        self.list_todo = self.list_todo + self._list_tp_ip(self.ip_discovered_list)
        self.list_todo = self.list_todo + self._dict_to_ip_list(self.cdp_info)
        self.list_todo = self.list_todo + self._dict_to_ip_list(self.bgp_info)

        self.list_complete = list(set(self.list_complete))
        self.list_todo = list(set(self.list_todo))

    def _add_list_to_todo(self):
        log.debug('starting: _add_list_to_todo')
        for item in self.list_todo:
            document = self._build_todo_obj(item)
            self.db2._todo_insert_todo(document)


    def _add_list_to_complete(self):
        log.debug('starting: _add_list_to_complete')
        for item in self.list_complete:
            document = self._build_todo_obj(item)
            self.db2._todo_insert_complete(document)

    def _add_list_to_cdp(self):
        log.debug('starting: _add_list_to_cdp')
        try:
            for item in self.cdp_info:
                self.db2.upsert_cdp(col=self.cfg['cdp'], doc=item)
        except Exception as e:
            log.error('error: {0}'.format(str(e)))

    def _add_inventory(self):
        log.debug('starting: _add_inventory')
        self.new_inventory = {"host_ip": self.new_device['ip_address'],
            "inventory": self.inventory}
        self.db2.add_document(col=self.cfg['inventory'], doc=self.new_inventory)

    def _add_arp(self):
        log.debug('starting: _add_arp')
        try:
            for item in self.arp_info:
                self.db2.upsert_arp(col=self.cfg['cdp'], doc=item)
        except Exception as e:
            log.error('error: {0}'.format(str(e)))


    def check_for_vrf(self):
        # standard start config: start
        self.abs_start(method_name = 'check_for_vrf')
        # standard start config: end

        self.director.builder = lib.show_ip_vrf.ShowIPVRF()
        self.director.construct_container()
        container = self.director.get_container()
        cmd_output = self.ssh_session.child_execute(command=container.cmd)
        self.director.container_filter(cmd_output)
        result = self.director.get_container()
        if len(result.regex_result) > 0:
            self.vrf = self.vrf + result.regex_result

        # standard start config: start
        self.abs_end(method_name='check_for_vrf')
        # standard start config: end

    def loop_show_ip_route(self, vrf_name):
        # standard start config: start
        method_name = 'loop_show_ip_route'
        self.abs_start(method_name = method_name)
        # standard start config: end

        self.director.builder = lib.show_ip_route.ShowIPRoute()
        self.director.construct_container(vrf_name=vrf_name)
        container = self.director.get_container()
        cmd_output = self.ssh_session.child_execute(command=container.cmd)
        self.director.container_filter(cmd_output)
        result = self.director.get_container()
        self.ip_discovered_list = self.ip_discovered_list + result.regex_result

        # standard start config: start
        self.abs_end(method_name='loop_show_ip_route')
        # standard start config: end

    def main_loop(self):
        # standard start config: start
        method_name = 'main_loop'
        self.abs_start(method_name = 'main_loop')
        # standard start config: end
        for method in self.function_list:
            # standard start config: start
            try:
                self.abs_start(method_name = method['description'])
                # standard start config: end
                self.director.builder = method['name']()
                self.director.construct_container()
                container = self.director.get_container()
                cmd_output = self.ssh_session.child_execute(command=container.cmd)
                self.director.container_filter(cmd_output)
                result = self.director.get_container()
                setattr(self, method['description'], result.regex_result)
                # standard start config: start
                self.abs_end(method_name = method['description'])
                # standard start config: end
            except Exception as e:
                log.error('{0}:exception:'.format(method['description']))
                log.error('{0}:error: {1}'.format(method['description'], str(e)))
                doc = {"ip_address": self.new_device['ip_address'], "error": str(e)}
                self.db2.add_document(col=self.cfg['remediation'], doc=doc)
                # standard start config: start
                self.abs_end(method_name= method['description'])
                # standard start config: end
        # standard start config: start
        self.abs_end(method_name='main_loop')
        # standard start config: end

    def start_ssh_session(self):
        # standard start config: start
        method_name = 'start_ssh_session'
        self.abs_start(method_name = 'start_ssh_session')
        # standard start config: end
        try:
            document = self._build_todo_obj(self.new_device['ip_address'])
            result = self.db2._todo_insert_complete(document)
            log.info('{0}:add doc: {1}'.format(method_name, result))
            self.ssh_session = helpers.ssh_child.SSHChild(
                host=self.new_device['ip_address'],
                #host='172.22.0.10',
                un=self.cfg['default_info']['un'],
                pw=self.cfg['default_info']['pw'],
                port=self.cfg['default_info']['port'])
            log.debug('{0}:success: {1}'.format(
                method_name, self.ssh_session))
            # standard start config: start
            self.abs_end(method_name='start_ssh_session')
            # standard start config: end
        except Exception as e:
            log.error('{0}:exception:'.format(method_name))
            log.error('{0}:error: {1}'.format(method_name, str(e)))
            raise
            # standard start config: start
            self.abs_end(method_name='start_ssh_session')
            # standard start config: end

    def get_function_list(self):
        self.function_list = lib.mapping.return_function_list(self)

    def get_vrf_function_list(self):
        self.function_list = lib.mapping.return_vrf_function_list(self)
    # Start and End Abstract

    def abs_start(self, method_name):
        self.set_time(method_name=method_name, action='_start')
        log.debug('{0}: starting'.format(method_name))
    def abs_end(self, method_name):
        self.set_time(method_name=method_name, action='_finish')
        self.execution_time(method_name=method_name)
        log.debug('{0}: ending'.format(method_name))
    # Performance Helper Methods
    def set_time(self, method_name, action):
        self.stats[method_name + action] = time.time()
    def execution_time(self, method_name):
        self.stats[method_name + '_exec_time'] = (self.stats[method_name + '_finish'] -
            self.stats[method_name + '_start'])
# Client
if __name__ == "__main__":
    client = BuildContainers()
    client.main()