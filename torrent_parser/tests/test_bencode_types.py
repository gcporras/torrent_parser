# -*- coding: utf-8 -*-
import pytest

from torrent_parser.bencode_types import (
    BencodeTypeError,
    get_bencode_type
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
    assert "Unknown data structure type" in str(excinfo.value)
