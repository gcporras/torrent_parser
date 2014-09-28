# -*- coding: utf-8 -*-
import pytest

from torrent_parser import errors
from torrent_parser.bencode_types import (
    BencodeTypeError,
    get_bencode_type,
    bencode_integer_is_valid
)


def test_get_bencode_types():
    """ Test that data structure types are correctly identified. """
    assert get_bencode_type("i463e") == int
    assert get_bencode_type("4:data") == str
    assert get_bencode_type("l4:spami42ee") == list
    assert get_bencode_type("d3:bar4:spam3:fooi42ee") == dict


def test_get_unknown_bencode_type_raises_exception():
    with pytest.raises(BencodeTypeError) as excinfo:
        get_bencode_type("UnknownDataType")
    assert errors.ERROR_BENCODE_UNKNOWN_DATA_TYPE in str(excinfo.value)


class TestBencodeIntegerValidation:
    @pytest.mark.parametrize("input,expected", [
        ("i34e", True),
        ("i345567745e", True),
        ("i-4523e", True),
    ])
    def test_bencode_integer_valid_values(self, input, expected):
        assert bencode_integer_is_valid(input) == expected

    def test_bencode_integer_invalid_no_end(self):
        with pytest.raises(BencodeTypeError) as excinfo:
            bencode_integer_is_valid("i2348")
        assert errors.ERROR_BENCODE_INTEGER_NO_END in str(excinfo.value)

    def test_bencode_integer_invalid_negative_zero(self):
        with pytest.raises(BencodeTypeError) as excinfo:
            bencode_integer_is_valid("i-0e")
        assert errors.ERROR_BENCODE_INTEGER_NEGATIVE_ZERO in str(excinfo.value)

    def test_bencode_integer_invalid_leading_zeros(self):
        with pytest.raises(BencodeTypeError) as excinfo:
            bencode_integer_is_valid("i024e")
        assert errors.ERROR_BENCODE_INTEGER_LEADING_ZEROS in str(excinfo.value)
