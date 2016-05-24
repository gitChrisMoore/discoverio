import unittest
import shutil, tempfile
from os import path
import env
from discoverio.mixins import valid_ip
from discoverio.mixins import build_ip_dict
from discoverio.mixins import adapt_cdp_dict
from discoverio.mixins import make_todo_list
from discoverio.mixins import make_completed_list
from discoverio.mixins import make_cdp_list
from discoverio.mixins import make_inventory_list

d = {'arp': [],
     'int': [{'int': '1.1.1.1'}, {'int': '2.2.2.2'}, {'int': '3.3.3.3'}
             ], 'route': [],
     'bgp': [{'neighbor_ip': '1.1.1.1', 'neighbor_router_id': '2.2.2.2'}],
     'eigrp': [],
     'cdp': [
         {'platform': 'cisco ASR1001', 'local_interface': 'GigabitEthernet0/0/1', 'capabilities': 'Router IGMP \r',
          'entry_ip_address': '5.5.5.5', 'advertisement_version': '2\r', 'holdtime': '147 sec\r',
          'remote_interface': 'remote_int_1/0/6\r'},
         {'platform': 'cisco ASR1001', 'local_interface': 'GigabitEthernet0/0/2', 'capabilities': 'Router IGMP \r',
          'entry_ip_address': '6.6.6.6', 'advertisement_version': '2\r', 'holdtime': '153 sec\r',
          'remote_interface': 'remote_int_1/0/4\r'},
         {'vtp_management_domain': "'vtp_tst_a'\r", 'platform': 'cisco WS-C3750E-24TD', 'duplex': 'full\r',
          'local_interface': 'GigabitEthernet0/0/3', 'capabilities': 'Router Switch IGMP \r',
          'entry_ip_address': '7.7.7.7', 'advertisement_version': '2\r', 'holdtime': '144 sec\r',
          'remote_interface': 'remote_int_1/0/5\r'}],
     'inventory': [{'vid': 'V05 ', 'pid': 'CISCO1941/K9      ', 'name': 'CISCO1941/K9', 'descr': 'CISCO1941/K9 chassis',
                    'sn': 'SN_Serial'}, {'vid': 'V01 ', 'pid': 'VWIC3-1MFT-T1/E1  ',
                                         'name': 'VWIC3-1MFT-T1/E1 - 1-Port RJ-48 Multiflex Trunk - T1/E1'
                                                 ' on Slot 0 SubSlot 0',
                                         'descr': 'VWIC3-1MFT-T1/E1 - 1-Port RJ-48 Multiflex Trunk - T1/E1',
                                         'sn': 'SN_Serial_B'},
                   {'vid': '   ', 'pid': 'PWR-1941-2901-AC  ', 'name': 'C1941/C2901 AC Power Supply',
                    'descr': 'C1941/C2901 AC Power Supply', 'sn': None}]}


class TestValidIp(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_private(self):
        # Create a file in the temporary directory

        self.assertTrue(valid_ip('1.1.1.2'))
        self.assertFalse(valid_ip('1.1.1.257'))
        self.assertTrue(valid_ip('1.1.1.2'))


class TestBuildIpDict(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_private(self):
        self.assertTrue(build_ip_dict('1.1.1.1'))
        self.assertFalse(build_ip_dict('1.1.1.257'))
        self.assertTrue(build_ip_dict('1.1.1.2'))


class TestAdaptCdpDict(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_private(self):
        self.assertTrue(adapt_cdp_dict({"entry_ip_address": "1.1.1.1"}))
        self.assertFalse(adapt_cdp_dict({"test": "hi"}))


class TestMakeTodoList(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_private(self):
        self.assertTrue(len(make_todo_list(d)) == 8)


class TestMakeCompletedList(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_private(self):
        self.assertTrue(len(make_completed_list(d)) == 3)


class TestMakeCdpList(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_private(self):
        self.assertTrue(len(make_cdp_list(d)) == 3)


class TestMakeInventoryList(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_private(self):
        self.assertTrue(len(make_inventory_list(d)) == 3)


if __name__ == '__main__':
    unittest.main()
