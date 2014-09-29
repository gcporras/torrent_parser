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


def bencode_string_is_valid(bstring):
    """
    Validate a bencoded string:
    A byte string (a sequence of bytes, not necessarily characters) is encoded as <length>:<contents>. The length is
    encoded in base 10, like integers, but must be non-negative (zero is allowed); the contents are just the bytes
    that make up the string. The string "spam" would be encoded as 4:spam.
    """
    try:
        colon = bstring.index(":")
    except ValueError:
        raise BencodeTypeError(errors.ERROR_BENCODE_STRING_MISSING_COLON, bstring)

    # String length must be a positive integer
    if not bstring[:colon].isdigit():
        raise BencodeTypeError(errors.ERROR_BENCODE_STRING_INVALID_LENGTH, bstring)

    return True


def decode_integer(binteger):
    """
    Decodes the bencoded integer representation and returns the integer.
    """
    if bencode_integer_is_valid(binteger):
        return int(binteger[1:binteger.index("e")])


def decode_string(bstring):
    """
    Decodes the bencoded string representation and returns the string.
    """
    if bencode_string_is_valid(bstring):
        colon = bstring.index(":")
        length = int(bstring[:colon])
        colon += 1
        return bstring[colon:colon+length]


def decode_list(blist):
    """
    Decodes the bencoded list representation and returns the decoded list.
    """
    if blist == "le":
        return []
