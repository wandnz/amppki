""" Common functions used by both the webscripts and the cli tools """

from re import search


def verify_common_name(name):
    """ Check that only valid characters are used in this hostname """

    if search("[^a-zA-Z0-9.-]+", name) is None:
        return True
    return False
