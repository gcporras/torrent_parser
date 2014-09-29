# -*- coding: utf-8 -*-
import pytest

from torrent_parser import errors
from torrent_parser.bencode_types import (
    BencodeTypeError,
    bencode_integer_is_valid,
    bencode_string_is_valid,
    decode_dict,
    decode_integer,
    decode_string,
    decode_list,
    find_data_structure_end,
    get_bencode_type,
    get_item
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


class TestBencodedStringValidation:
    @pytest.mark.parametrize("input,expected", [
        ("4:spam", True),
        ("0:", True),
        ("35:udp://tracker.openbittorrent.com:8013", True),
    ])
    def test_bencode_string_valid_values(self, input, expected):
        assert bencode_string_is_valid(input) == expected

    def test_bencode_string_invalid_no_colon(self):
        with pytest.raises(BencodeTypeError) as excinfo:
            bencode_string_is_valid("4spam")
        assert errors.ERROR_BENCODE_STRING_MISSING_COLON in str(excinfo.value)

    def test_bencode_string_invalid_no_digit_before_colon(self):
        with pytest.raises(BencodeTypeError) as excinfo:
            bencode_string_is_valid("4e:toto")
        assert errors.ERROR_BENCODE_STRING_INVALID_LENGTH in str(excinfo.value)


class TestDecodeBencodeBasicDataTypes:
    @pytest.mark.parametrize("input,expected", [
        ("i34e", 34),
        ("i345567745e", 345567745),
        ("i-4523e", -4523),
    ])
    def test_bencode_decode_integer(self, input, expected):
        assert decode_integer(input) == expected

    @pytest.mark.parametrize("input,expected", [
        ("4:spam", "spam"),
        ("0:", ""),
    ])
    def test_bencode_decode_string(self, input, expected):
        assert decode_string(input) == expected


class TestFindDataStructureEnd:
    def test_find_data_end_for_list_with_integer(self):
        bdata = "l4:spame3:end"
        end = find_data_structure_end(bdata, 1)
        assert bdata[:end] == "l4:spame"

    def test_find_data_end_for_nested_dict(self):
        bdata = "d5:gcp007:value_ed5:key_1e7:value_2ei1e"
        end = find_data_structure_end(bdata, 1)
        assert bdata[:end] == "d5:gcp007:value_ed5:key_1e7:value_2e"


class TestGetItems:
    @pytest.mark.parametrize("input,expected", [
        ("i34e", ["i34e"]),
        ("i3ei45e", ["i3e", "i45e"]),
        ("4:spam", ["4:spam"]),
        ("i34e4:spam", ["i34e", "4:spam"]),
        ("4:spami1e3:cat", ["4:spam", "i1e", "3:cat"]),
        ("li1ee", ["li1ee"]),
        ("di12ee", ["di12ee"]),
        ("d3:subd4:yoyo2:reeei88e", ['d3:subd4:yoyo2:reee', 'i88e']),
        ("li45el3:catei3eeli1ee", ['li45el3:catei3ee', 'li1ee'])
    ])
    def test_get_items(self, input, expected):
        assert get_item(input) == expected


class TestDecodeBencodeLists:
    @pytest.mark.parametrize("input,expected", [
        ("le", []),
        ("lli1ei2eeli3ei4eee", [[1, 2], [3, 4]]),
        ("l3:cat2:doli2e1:Tee", ['cat', 'do', [2, 'T']])
    ])
    def test_bencode_decode_list(self, input, expected):
        assert decode_list(input) == expected


class TestDecodeBencodeDicts:
    @pytest.mark.parametrize("input,expected", [
        ("de", []),
        ("d3:key5:valuee", {"key": "value"}),
        ("d3:keyd3:key5:valueee", {'key': {'key': 'value'}}),
        ("d3:keyl6:value16:value2ee", {'key': ["value1", "value2"]})
    ])
    def test_bencode_decode_dict(self, input, expected):
        assert decode_dict(input) == expected
