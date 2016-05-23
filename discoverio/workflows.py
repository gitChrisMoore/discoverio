"""
The intent of this file is to provide a place to loop through workflows.

The structure of the chain should go as follows:

    regex_split

    loop_through_output
        for entry in output list:
        return dict_array

            loop_through_regex
                for entry in regex list:
                return dict
"""

import re


def regex(regex_cmd, output_segment):
    """
    This takes in a regex and command output, and returns a value if found

    :param regex_cmd:
    :param output_segment:
    :return:
    """
    def _regex():
        try:
            return re.search(regex_cmd, output_segment).group(1)
        except Exception as e:
            pass

    return _regex()


def regex_split(original_output, regex_split_cmd):
    """
    Takes in a regex string and output, returns a list of output split

    :param original_output:
    :param regex_split_cmd:
    :return:
    """

    def _regex_split():
        return original_output.split(regex_split_cmd)

    return _regex_split()


def loop_through_output(output_list, regex_list):
    """
    This manages the loop through the split list of output, returns a dict array

    :param output_list:
    :param regex_list:
    :return:
    """

    def _loop_through_output():
        dict_array = []

        for output_segment in output_list:
            dict = loop_through_regex(output_segment, regex_list)
            if dict.values()[0]:
                dict_array.append(dict)
        return dict_array

    return _loop_through_output()


def loop_through_regex(output_segment, regex_list):
    """
    This manages the loop through individual regex commands, returns a dict

    :param output_segment:
    :param regex_list:
    :return:
    """
    def _loop_through_regex():
        d = {}
        for i in regex_list:
            try:
                d[i['item_property']] = regex(i['regex_syntax'], output_segment)
            except:
                pass
        return d

    return _loop_through_regex()

