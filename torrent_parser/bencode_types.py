# -*- coding: utf-8 -*-
class BencodeTypeError(Exception):
    """
    Raised if an error occurs while parsing Bencode data
    """

    def __init__(self, value, data):
        self.value = value
        self.data = data

    def __str__(self):
        return repr(self.value + " : " + str(self.data))


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
    else:
        raise BencodeTypeError("Unknown data structure type", data)
