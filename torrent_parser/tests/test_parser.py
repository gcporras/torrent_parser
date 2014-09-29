# -*- coding: utf-8 -*-
from torrent_parser.parser import TorrentParser


class TestGetTaskInformations:
    def test_can_obtain_tracker_url(self):
        torrent_parser = TorrentParser("torrent_parser/tests/test_data/ElephantsDream(avi)(1024x576).torrent")
        assert "http://jip.cs.vu.nl:6969/announce" == torrent_parser.get_tracker_url()
