# -*- coding: utf-8 -*-
from exceptions import *
from tiles import *


class AIException(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)

    def __repr__(self):
        return self.__str__()


class DummyAI:

    def __init__(self):
        self.game = None
        self.player = None


    def discard(self):
        for i in range(Tiles.NUM):
            index = Tiles.NUM - i - 1
            if self.player.tiles[index] != 0:
                return index


    def chow(self, tile):
        return False


    def pung(self, tile):
        return False


    def bigMeldedKong(self, tile):
        return False


    def smallMeldedKong(self):
        return False


    def concealedKong(self):
        return False