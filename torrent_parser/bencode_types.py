# -*- coding: utf-8 -*-
from torrent_parser import errors


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
        raise BencodeTypeError(errors.ERROR_BENCODE_UNKNOWN_DATA_TYPE, data)


def bencode_integer_is_valid(binteger):
    """
    Validates a bencoded integer:
    An integer is encoded as i<integer encoded in base ten ASCII>e. Leading zeros are not allowed (although the number
    zero is still represented as "0"). Negative values are encoded by prefixing the number with a minus sign. The
    number 42 would thus be encoded as i42e, 0 as i0e, and -42 as i-42e. Negative zero is not permitted.
    """
    try:
        end = binteger.index("e")
    except ValueError:
        raise BencodeTypeError(errors.ERROR_BENCODE_INTEGER_NO_END, binteger)

    integer_value = binteger[1:end]

    if len(integer_value) > 1:
        # A negative zero is not permitted
        if integer_value[0] == "-" and integer_value[1] == "0":
            raise BencodeTypeError(errors.ERROR_BENCODE_INTEGER_NEGATIVE_ZERO, binteger)

        # Leading zeros are note allowed
        if integer_value[0] == "0":
            raise BencodeTypeError(errors.ERROR_BENCODE_INTEGER_LEADING_ZEROS, binteger)

    return True
