# -*- coding: utf-8 -*-
def get_bencode_type(data):
    """
    Returns the type of a `Bencode <http://en.wikipedia.org/wiki/Bencode>`_ data structure
    """
    type_identifier = data[0]

    if type_identifier.isdigit():
        return str
    elif type_identifier == "i":
        return int
    elif type_identifier == "l":
        return list
    elif type_identifier == "d":
        return dict
