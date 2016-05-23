#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
config.py
-------------------
Global configuration handling
"""


def valid_path(file_path=None):
    """
     Takes in relative path variable, returns path if true.

    :param file_path:
    :return:
    """
    import os

    if not file_path:
        raise Exception('No path provided')
    path = os.path.dirname(os.path.abspath(__file__))
    path += file_path

    def _valid_path(*args, **kwargs):
        if os.path.exists(path):
            return path
        else:
            raise Exception('Path variable present, but not a valid path. var: ' + path)

    return _valid_path()


def load_json(path):
    """
    Takes in valid file path, returns dict of json output

    :param path:
    :return:
    """
    import json

    def _load_json(*args, **kwargs):
        with open(path) as data_file:
            return json.load(data_file)

    return _load_json()


def set_config(pri='/private.json', pub='/public.json'):
    """
    Uses the defaults to load in the private and public config, returns dict

    :param pri:
    :param pub:
    :return:
    """
    path_pri = valid_path(pri)
    path_pub = valid_path(pub)
    d0 = load_json(path_pri)
    d1 = load_json(path_pub)

    def _set_config(*args, **kwargs):
        d3 = dict(d0)
        d3.update(d1)
        return d3

    return _set_config()

