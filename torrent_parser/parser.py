# -*- coding: utf-8 -*-
from torrent_parser.bencode_types import decode
import codecs


class TorrentParser():
    def __init__(self, file_name):
        self.torrent_file = codecs.open(file_name).read()
        self.torrent_dict = decode(self.torrent_file)

    def get_tracker_url(self):
        return self.torrent_dict['announce']
