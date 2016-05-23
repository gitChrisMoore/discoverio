import unittest
import shutil, tempfile
from os import path
import env
from discoverio.mapping import mapping
from discoverio.workflows import loop_through_output
from discoverio.workflows import regex_split

test_arp = ("Router#show ip arp vrf MPLS\n"
            "Protocol  Address          Age (min)  Hardware Addr   Type   Interface\n"
            "Internet  10.0.1.13             -   56bc.56bc.389a  ARPA   GigabitEthernet0/0/0\n"
            "Internet  10.0.1.14           218   56bc.389a.31e9  ARPA   GigabitEthernet0/0/0\n"
            "Internet  10.0.1.25             -   56bc.56bc.389a  ARPA   GigabitEthernet0/1/3\n"
            "Internet  10.0.1.26             3   56bc.389a.5f8e  ARPA   GigabitEthernet0/1/3\n"
            "Internet  10.0.1.65             -   56bc.56bc.389a  ARPA   GigabitEthernet0/1/2.50\n"
            "Internet  10.0.1.66            91   56bc.389a.f9f2  ARPA   GigabitEthernet0/1/2.50\n"
            "Router#")

test_cdp = ("\n"
            "switchS#show cdp neighbors detail\n"
            "-------------------------\n"
            "Device ID: Switch_A.intranet.local\n"
            "Entry address(es):\n"
            "  IP address: 1.1.1.1\n"
            "Platform: cisco WS-C4506,  Capabilities: Router Switch IGMP\n"
            "Interface: GigabitEthernet0/1,  Port ID (outgoing port): GigabitEthernet5/12\n"
            "Holdtime : 135 sec\n"
            "\n"
            "Version :\n"
            "Cisco IOS Software, Catalyst 4500 L3 Switch Software (cat4500-ENTSERVICESK9-M), Version 12.2(46)SG, RELEASE SOFTWARE (fc1)\n"
            "Technical Support: http://www.cisco.com/techsupport\n"
            "Copyright (c) 1986-2008 by Cisco Systems, Inc.\n"
            "Compiled Fri 27-Jun-08 16:24 by prod_rel_team\n"
            "\n"
            "advertisement version: 2\n"
            "VTP Management Domain: 'Dist1-Access'\n"
            "Duplex: full\n"
            "Management address(es):\n"
            "  IP address: 1.1.1.1\n"
            "\n"
            "-------------------------\n"
            "Device ID: Switch_B.intranet.local\n"
            "Entry address(es):\n"
            "  IP address: 2.2.2.2\n"
            "Platform: cisco WS-C4506,  Capabilities: Router Switch IGMP\n"
            "Interface: GigabitEthernet0/4,  Port ID (outgoing port): GigabitEthernet5/12\n"
            "Holdtime : 123 sec\n"
            "\n"
            "Version :\n"
            "Cisco IOS Software, Catalyst 4500 L3 Switch Software (cat4500-ENTSERVICESK9-M), Version 12.2(46)SG, RELEASE SOFTWARE (fc1)\n"
            "Technical Support: http://www.cisco.com/techsupport\n"
            "Copyright (c) 1986-2008 by Cisco Systems, Inc.\n"
            "Compiled Fri 27-Jun-08 16:24 by prod_rel_team\n"
            "\n"
            "advertisement version: 2\n"
            "VTP Management Domain: 'Dist1-Access'\n"
            "Duplex: full\n"
            "Management address(es):\n"
            "  IP address: 2.2.2.2\n"
            "\n"
            "Switch#")

test_inv = ('Router#show inventory\n'
            'NAME: "CISCO1941/K9", DESCR: "CISCO1941/K9 chassis, Hw Serial#: HW_Serial, Hw Revision: 1.0"\n'
            'PID: CISCO1941/K9      , VID: V05 , SN: SN_Serial\n'
            '\n'
            'NAME: "VWIC3-1MFT-T1/E1 - 1-Port RJ-48 Multiflex Trunk - T1/E1 on Slot 0 SubSlot 0", DESCR: "VWIC3-1MFT-T1/E1 - 1-Port RJ-48 Multiflex Trunk - T1/E1"\n'
            'PID: VWIC3-1MFT-T1/E1  , VID: V01 , SN: SN_Serial_B\n'
            '\n'
            'NAME: "C1941/C2901 AC Power Supply", DESCR: "C1941/C2901 AC Power Supply"\n'
            'PID: PWR-1941-2901-AC  , VID:    , SN:\n'
            '\n')

test_route = ("Router#show ip route vrf Internet\n"
              "\n"
              "Routing Table: Internet\n"
              "Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP\n"
              "       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area\n"
              "       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2\n"
              "       E1 - OSPF external type 1, E2 - OSPF external type 2\n"
              "       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2\n"
              "       ia - IS-IS inter area, * - candidate default, U - per-user static route\n"
              "       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP\n"
              "       a - application route\n"
              "       + - replicated route, % - next hop override\n"
              "\n"
              "Gateway of last resort is 1.1.1.1 to network 0.0.0.0\n"
              "\n"
              "S*    0.0.0.0/0 [1/0] via 2.2.2.1\n"
              "      10.20.0.0/16 is variably subnetted, 2 subnets, 2 masks\n"
              "C        10.20.240.0/21 is directly connected, GigabitEthernet0/0/1\n"
              "L        10.20.241.236/32 is directly connected, GigabitEthernet0/0/1\n"
              "BR21-WAN-2-A#show ip route vrf VPN\n"
              "\n"
              "Routing Table: VPN\n"
              "Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP\n"
              "       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area\n"
              "       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2\n"
              "       E1 - OSPF external type 1, E2 - OSPF external type 2\n"
              "       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2\n"
              "       ia - IS-IS inter area, * - candidate default, U - per-user static route\n"
              "       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP\n"
              "       a - application route\n"
              "       + - replicated route, % - next hop override\n"
              "\n"
              "Gateway of last resort is 172.29.9.1 to network 0.0.0.0\n"
              "\n"
              "B*    0.0.0.0/0 [20/27392] via 1.1.1.1 (WAN), 2d08h, GigabitEthernet0/0/2\n"
              "      10.0.0.0/8 is variably subnetted, 434 subnets, 14 masks\n"
              "B        10.0.0.0/8\n"
              "           [20/27648] via 1.1.1.2 (WAN), 7w0d, GigabitEthernet0/0/2\n"
              "B        10.126.0.0/21 [200/0] via 10.0.0.2, 05:36:43\n"

              "BR21-WAN-2-A#")

test_vrf = ("Router#show vrf detail\n"
            "VRF IPv6Internet (VRF Id = 6); default RD 65000:11; default VPNID <not set>\n"
            "  New CLI format, supports multiple address-families\n"
            "  Flags: 0x180C\n"
            "  Interfaces:\n"
            "    Gi0/1/4                 \n"
            "Address family ipv4 unicast not active\n"
            "Address family ipv6 unicast (Table ID = 0x1E000002):\n"
            "  Flags: 0x0\n"
            "  No Export VPN route-target communities\n"
            "  No Import VPN route-target communities\n"
            "  No import route-map\n"
            "  No global export route-map\n"
            "  No export route-map\n"
            "  VRF label distribution protocol: not configured\n"
            "  VRF label allocation mode: per-prefix\n"
            "Address family ipv4 multicast not active\n"
            "\n"
            "VRF Internet (VRF Id = 2); default RD 65000:10; default VPNID <not set>\n"
            "  Old CLI format, supports IPv4 only\n"
            "  Flags: 0xC\n"
            "  Interfaces:\n"
            "    Gi0/0/1                 \n"
            "Address family ipv4 unicast (Table ID = 0x2):\n"
            "  Flags: 0x0\n"
            "  No Export VPN route-target communities\n"
            "  No Import VPN route-target communities\n"
            "  No import route-map\n"
            "  No global export route-map\n"
            "  No export route-map\n"
            "  VRF label distribution protocol: not configured\n"
            "  VRF label allocation mode: per-prefix\n"
            "Address family ipv6 unicast not active\n"
            "Address family ipv4 multicast not active\n"
            "\n"
            "VRF MPLS (VRF Id = 3); default RD 65000:1; default VPNID <not set>\n"
            "  Old CLI format, supports IPv4 only\n"
            "  Flags: 0xC\n"
            "  Interfaces:\n"
            "    Lo3                      Gi0/0/0                  Gi0/1/0.53              \n"
            "    Gi0/1/1                  Gi0/1/2.50               Gi0/1/3                 \n"
            "Address family ipv4 unicast (Table ID = 0x3):\n"
            "  Flags: 0x0\n"
            "  Export VPN route-target communities\n"
            "    RT:65000:1              \n"
            "  Import VPN route-target communities\n"
            "    RT:65000:1               RT:65000:3              \n"
            "  No import route-map\n"
            "  No global export route-map\n"
            "  No export route-map\n"
            "  VRF label distribution protocol: not configured\n"
            "  VRF label allocation mode: per-prefix\n"
            "Address family ipv6 unicast not active\n"
            "Address family ipv4 multicast not active\n"
            "\n"
            "VRF Mgmt-intf (VRF Id = 1); default RD <not set>; default VPNID <not set>\n"
            "  New CLI format, supports multiple address-families\n"
            "  Flags: 0x1808\n"
            "  Interfaces:\n"
            "    Gi0                     \n"
            "Address family ipv4 unicast (Table ID = 0x1):\n"
            "  Flags: 0x0\n"
            "  No Export VPN route-target communities\n"
            "  No Import VPN route-target communities\n"
            "  No import route-map\n"
            "  No global export route-map\n"
            "  No export route-map\n"
            "  VRF label distribution protocol: not configured\n"
            "  VRF label allocation mode: per-prefix\n"
            "Address family ipv6 unicast (Table ID = 0x1E000001):\n"
            "  Flags: 0x0\n"
            "  No Export VPN route-target communities\n"
            "  No Import VPN route-target communities\n"
            "  No import route-map\n"
            "  No global export route-map\n"
            "  No export route-map\n"
            "  VRF label distribution protocol: not configured\n"
            "  VRF label allocation mode: per-prefix\n"
            "Address family ipv4 multicast not active\n"
            "\n"
            "VRF VPN (VRF Id = 4); default RD 65000:2; default VPNID <not set>\n"
            "  Old CLI format, supports IPv4 only\n"
            "  Flags: 0xC\n"
            "  Interfaces:\n"
            "    Lo1                      Lo2                      Tu1111                   \n"
            "    Tu1111                   Tu1111                   Tu1111                  \n"
            "    Tu1111                   Tu1111                  Tu1111                \n"
            "    Tu930                    Lo4                     \n"
            "Address family ipv4 unicast (Table ID = 0x4):\n"
            "  Flags: 0x0\n"
            "  Export VPN route-target communities\n"
            "    RT:65000:2              \n"
            "  Import VPN route-target communities\n"
            "    RT:65000:2               RT:65000:3              \n"
            "  No import route-map\n"
            "  No global export route-map\n"
            "  No export route-map\n"
            "  VRF label distribution protocol: not configured\n"
            "  VRF label allocation mode: per-prefix\n"
            "Address family ipv6 unicast not active\n"
            "Address family ipv4 multicast not active\n"
            "\n"
            "VRF WAN (VRF Id = 5); default RD 65000:3; default VPNID <not set>\n"
            "  Old CLI format, supports IPv4 only\n"
            "  Flags: 0xC\n"
            "  Interfaces:\n"
            "    Lo0                      Gi0/0/2                  Gi0/0/3                 \n"
            "Address family ipv4 unicast (Table ID = 0x5):\n"
            "  Flags: 0x0\n"
            "  Export VPN route-target communities\n"
            "    RT:65000:3              \n"
            "  Import VPN route-target communities\n"
            "    RT:65000:1               RT:65000:2               RT:65000:3\n"
            "  No import route-map\n"
            "  No global export route-map\n"
            "  No export route-map\n"
            "  VRF label distribution protocol: not configured\n"
            "  VRF label allocation mode: per-prefix\n"
            "Address family ipv6 unicast not active\n"
            "Address family ipv4 multicast not active")

test_bgp = ("Router# show bgp all neighbors\n"
            "For address family: IPv4 Unicast\n"
            "\n"
            "For address family: IPv6 Unicast\n"
            "\n"
            "For address family: VPNv4 Unicast\n"
            "BGP neighbor is 1.1.1.1,  vrf MPLS,  remote AS 11158, external link\n"
            "  BGP version 4, remote router ID 2.2.2.2\n"
            "  BGP state = Established, up for 4w6d\n"
            "  Last read 00:00:03, last write 00:00:01, hold time is 15, keepalive interval is 5 seconds\n"
            "  Configured hold time is 15, keepalive interval is 5 seconds\n"
            "  Minimum holdtime from neighbor is 0 seconds\n"
            "  Neighbor sessions:\n"
            "    1 active, is not multisession capable (disabled)\n"
            "  Neighbor capabilities:\n"
            "    Route refresh: advertised and received(new)\n"
            "    Four-octets ASN Capability: advertised and received\n"
            "    Address family IPv4 Unicast: advertised and received\n"
            "    Enhanced Refresh Capability: advertised\n"
            "    Multisession Capability: \n"
            "    Stateful switchover support enabled: NO for session 1\n"
            "  Message statistics:\n"
            "    InQ depth is 0\n"
            "    OutQ depth is 0\n"
            "    \n"
            "                         Sent       Rcvd\n"
            "    Opens:                  1          1\n"
            "    Notifications:          0          0\n"
            "    Updates:               13         94\n"
            "    Keepalives:        582113     662095\n"
            "    Route Refresh:          0          0\n"
            "    Total:             582127     662190\n"
            "  Default minimum time between advertisement runs is 0 seconds\n"
            "\n"
            "  Address tracking is enabled, the RIB does have a route to 10.160.1.14\n"
            "  Connections established 72; dropped 71\n"
            "  Last reset 4w6d, due to BGP Notification received of session 1, hold time expired\n"
            "  Transport(tcp) path-mtu-discovery is enabled\n"
            "  Graceful-Restart is disabled\n"
            "  SSO is disabled\n"
            "Connection state is ESTAB, I/O status: 1, unread input bytes: 0            \n"
            "Connection is ECN Disabled, Mininum incoming TTL 0, Outgoing TTL 1\n"
            "Local host: 3.3.3.3, Local port: 179\n"
            "Foreign host: 4.4.4.4, Foreign port: 51116\n"
            "Connection tableid (VRF): 3\n"
            "Maximum output segment queue size: 50\n"
            "\n"
            "Enqueued packets for retransmit: 0, input: 0  mis-ordered: 0 (0 bytes)\n"
            "\n"
            "Event Timers (current time is 0x8E5FBD537):\n"
            "Timer          Starts    Wakeups            Next\n"
            "Retrans        582127          5             0x0\n"
            "TimeWait            0          0             0x0\n"
            "AckHold        662157     621316             0x0\n"
            "SendWnd             0          0             0x0\n"
            "KeepAlive           0          0             0x0\n"
            "GiveUp              0          0             0x0\n"
            "PmtuAger            0          0             0x0\n"
            "DeadWait            0          0             0x0\n"
            "Linger              0          0             0x0\n"
            "ProcessQ            0          0             0x0\n"
            "\n"
            "iss: 1557775274  snduna: 1568836161  sndnxt: 1568836161\n"
            "irs:  506293354  rcvnxt:  518878319\n"
            "\n"
            "sndwnd:  16384  scale:      0  maxrcvwnd:  16384\n"
            "rcvwnd:  15814  scale:      0  delrcvwnd:    570\n"
            "\n"
            "SRTT: 1000 ms, RTTO: 1003 ms, RTV: 3 ms, KRTT: 0 ms\n"
            "minRTT: 65 ms, maxRTT: 1000 ms, ACK hold: 200 ms\n"
            "uptime: -1314520687 ms, Sent idletime: 612 ms, Receive idletime: 534 ms \n"
            "Status Flags: passive open, gen tcbs\n"
            "Option Flags: VRF id set, nagle, path mtu capable\n"
            "IP Precedence value : 6\n"
            "\n"
            "Datagrams (max data segment is 1024 bytes):\n"
            "Rcvd: 1244253 (out of order: 0), with data: 662169, total data bytes: 12584964\n"
            "Sent: 1218893 (retransmit: 5, fastretransmit: 0, partialack: 0, Second Congestion: 0), with data: 582125, total data bytes: 11060905\n"
            "\n"
            " Packets received in fast path: 0, fast processed: 0, slow path: 0\n"
            " fast lock acquisition failures: 0, slow path: 0\n"
            "TCP Semaphore      0x431F6390  FREE \n"
            "          \n"
            "BGP neighbor is 5.5.5.5,  vrf MPLS,  remote AS 209, external link\n"
            "  BGP version 4, remote router ID 6.6.6.6\n"
            "  BGP state = Established, up for 32w2d\n"
            "  Last read 00:00:01, last write 00:00:01, hold time is 15, keepalive interval is 5 seconds\n"
            "  Configured hold time is 15, keepalive interval is 5 seconds\n"
            "  Minimum holdtime from neighbor is 0 seconds\n"
            "  Neighbor sessions:\n"
            "    1 active, is not multisession capable (disabled)\n"
            "  Neighbor capabilities:\n"
            "    Route refresh: advertised and received(new)\n"
            "    Four-octets ASN Capability: advertised and received\n"
            "    Address family IPv4 Unicast: advertised and received\n"
            "    Enhanced Refresh Capability: advertised\n"
            "    Multisession Capability: \n"
            "    Stateful switchover support enabled: NO for session 1\n"
            "  Message statistics:\n"
            "    InQ depth is 0\n"
            "    OutQ depth is 0\n"
            "    \n")

test_eigrp = ("Router#   show ip eigrp vrf WAN neighbors \n"
              "EIGRP-IPv4 Neighbors for AS(1) VRF(WAN)\n"
              "H   Address                 Interface              Hold Uptime   SRTT   RTO  Q  Seq\n"
              "                                                   (sec)         (ms)       Cnt Num\n"
              "1   1.1.1.1             Gi0/0/3                  11 1y11w      19   114  0  989866\n"
              "0   2.2.2.2              Gi0/0/2                  14 1y11w       6   100  0  990031")

test_int = ("BR21-WAN-2-A#show ip int brief\n"
            "Interface              IP-Address      OK? Method Status                Protocol\n"
            "GigabitEthernet0/0/0   1.1.1.1     YES NVRAM  up                    up      \n"
            "GigabitEthernet0/0/1   2.2.2.2  YES NVRAM  up                    up      \n"
            "GigabitEthernet0/0/2   3.3.3.3      YES NVRAM  up                    up      \n"
            "GigabitEthernet0/0/3   4.4.4.4     YES NVRAM  up                    up      \n"
            "GigabitEthernet0/1/0   5.5.5.5      YES NVRAM  administratively down down    \n"
            "Gi0/1/0.53             6.6.6.6     YES NVRAM  administratively down down    \n"
            "GigabitEthernet0/1/1   unassigned      YES unset  administratively down down    ")


class TestMapping(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_private(self):
        # Create a file in the temporary directory
        self.assertTrue(len(mapping()) >= 0)


class TestWorkflowA(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_private(self):
        # Create a file in the temporary directory
        pass


class TestRegexSplit(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_private(self):
        l = mapping()
        for item in l:
            if 'arp' in item['name']:
                i = item
        split_result = regex_split(test_arp, i['regex_split'])
        result = loop_through_output(split_result, i['method_list'])
        self.assertTrue(len(result) == 6)


class TestRegexCdp(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_private(self):
        l = mapping()
        for item in l:
            if 'cdp' in item['name']:
                i = item
        split_result = regex_split(test_cdp, i['regex_split'])
        result = loop_through_output(split_result, i['method_list'])
        self.assertTrue(len(result) == 2)


class TestRegexInv(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_private(self):
        l = mapping()
        for item in l:
            if 'inv' in item['name']:
                i = item
        split_result = regex_split(test_inv, i['regex_split'])
        result = loop_through_output(split_result, i['method_list'])
        self.assertTrue(len(result) == 3)


class TestRegexRoute(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_private(self):
        l = mapping()
        for item in l:
            if 'route' in item['name']:
                i = item
        split_result = regex_split(test_route, i['regex_split'])
        result = loop_through_output(split_result, i['method_list'])
        self.assertTrue(len(result) == 4)


class TestRegexBgp(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_private(self):
        l = mapping()
        for item in l:
            if 'bgp' in item['name']:
                i = item
        split_result = regex_split(test_bgp, i['regex_split'])
        result = loop_through_output(split_result, i['method_list'])
        self.assertTrue(len(result) == 2)


class TestRegexEigrp(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_private(self):
        l = mapping()
        for item in l:
            if 'eigrp' in item['name']:
                i = item
        split_result = regex_split(test_eigrp, i['regex_split'])
        result = loop_through_output(split_result, i['method_list'])

        self.assertTrue(len(result) == 2)


class TestRegexVrf(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_private(self):
        l = mapping()
        for item in l:
            if 'vrf' in item['name']:
                i = item
        split_result = regex_split(test_vrf, i['regex_split'])
        result = loop_through_output(split_result, i['method_list'])
        self.assertTrue(len(result) == 6)


class TestRegexInt(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_private(self):
        l = mapping()
        for item in l:
            if 'int' in item['name']:
                i = item
        split_result = regex_split(test_int, i['regex_split'])
        result = loop_through_output(split_result, i['method_list'])
        self.assertTrue(len(result) == 6)


if __name__ == "__main__":
    unittest.main()
