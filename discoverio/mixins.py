"""

The make lists at the bottom can be consolidated, as they really do similar functions
it was easier though to get the tests to run as is.

All modules in this folder are passing as of Sunday, Mas 22, 2016

Todo:
    Change print to logging
    Consolidate the to list functions

"""


def valid_ip(ip):
    """
    Takes in ip address as string, validates that it is ip address

    :param ip:
    :return:
    """
    import re
    test_ip = ip

    def _valid_ip(ip):
        try:
            valid_ip_regex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}" \
                                  "([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
            return re.match(valid_ip_regex, test_ip).group()
        except Exception as e:
            #print 'Not a valid ip: ip: {} error {}'.format(str(e), test_ip)
            return

    return _valid_ip(test_ip)


def build_ip_dict(ip):
    """
    Takes in ip address as string, if valid IP, builds a dictionary
    :param ip:
    :return:
    """

    inner_ip = ip

    def _build_ip_dict(inner_ip):
        if valid_ip(inner_ip):
            return {"ip address": inner_ip}

    if type(inner_ip) is dict:
        if 'entry_ip_address' in inner_ip:
            return _build_ip_dict(inner_ip['entry_ip_address'])
    else:
        return _build_ip_dict(inner_ip)


def adapt_cdp_dict(d):
    """
    Takes in cdp dictionary, if entry_ip_address field exists, returns a dict edited
    :param d:
    :return:
    """
    outer_d = d

    def _adapt_cdp_dict(outer_d):
        try:
            if outer_d['entry_ip_address']:
                outer_d['ip_address'] = outer_d['entry_ip_address']
                return outer_d
            else:
                return False
        except KeyError as ke:
            #print 'Not a valid key: d: {} error {}'.format(str(ke), outer_d)
            return

    return _adapt_cdp_dict(outer_d)


def make_todo_list(d):
    """
    Takes in a dictionary, returns a formated list of ip valid ip address.

    :param d:
    :return:
    """
    outer_d = d

    def _make_todo_list(outer_d):

        l = [v
             for key, value in outer_d.iteritems()
             for v in value
             if key == 'route' or key == 'bgp' or key == 'eigrp' or key == 'arp' or key == 'cdp']

        a = [build_ip_dict(v)
             for item in l
             for k, v in item.iteritems()]
        return filter(None, a)

    return _make_todo_list(outer_d)


def make_completed_list(d):
    """
    Takes in dict of node, returns a list of ip addresses which device owns

    :param d:
    :return:
    """
    outer_d = d

    def _make_completed_list(outer_d):

        l = [v
             for key, value in outer_d.iteritems()
             for v in value
             if key == 'int']

        a = [build_ip_dict(v)
             for item in l
             for k, v in item.iteritems()]
        return filter(None, a)

    return _make_completed_list(outer_d)


def make_cdp_list(d):
    """
    Takes in dict of device, returns list of cdp neighbors

    :param d:
    :return:
    """
    outer_d = d

    def _make_cdp_list(outer_d):

        l = [adapt_cdp_dict(v)
             for key, value in outer_d.iteritems()
             for v in value
             if key == 'cdp']
        return filter(None, l)

    return _make_cdp_list(outer_d)


def make_inventory_list(d):
    """
    Takes in dict of device from discovery, returns list of inventory

    :param d:
    :return:
    """
    outer_d = d

    def _make_cdp_list(outer_d):

        l = [v
             for key, value in outer_d.iteritems()
             for v in value
             if key == 'inventory']
        return filter(None, l)

    return _make_cdp_list(outer_d)

