# -*- coding: utf-8 -*-

TESTSUITE_TEMPLATE = u'test'
TESTSUITE_DIRECTORY = u'directory'


import os
from . import config
from error import TestsuiteError


def check(id_):
    try:
        info = get_info(id_)
        if info['type'] == TESTSUITE_TEMPLATE:
            return True
        else:
            return False
    except TestsuiteError:
        return False
    except KeyError:
        return False


def get_info(id_):
    return get_data(id_)


def get_name(id_):
    pass


def get_data(id_):
    return config.get_data(os.path.join(id_, config.OPTIONS_FILE))


def get_list(path):
    ls = []
    try:
        for root, dirs, files in os.walk(path):
            for name in dirs:
                if check(os.path.join(root, name)):
                    type = TESTSUITE_TEMPLATE
                else:
                    type = TESTSUITE_DIRECTORY
                ls.append((name, type))
            break
    except OSError as e:
        print u'could not list directory: ' + e.strerror
    return ls
