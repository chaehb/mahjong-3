# -*- coding: utf-8 -*-

from tiles import *
from ai import *

class Player:

    def __init__(self, ai):
        self.ai = ai
        self.ai.player = self
        self.seatWind = None
        self.tiles = Tiles()
        self.meldedTileSets = []


    def draw(self, tile):
        self.tiles.add(tile)


    def discard(self):
        t = self.ai.discard()
        if self.tiles[t] > 0:
            self.tiles[t] -= 1
            return t

        else:
            raise AIException('Error When Discarding: ' + str(t))


    def chow(self, tile):
        return self.ai.chow(tile)


    def pung(self, tile):
        return self.ai.pung(tile)


    def bigMeldedKong(self, tile):
        return self.ai.bigMeldedKong(tile)


    def smallMeldedKong(self):
        return self.ai.smallMeldedKong()


    def concealedKong(self):
        return self.ai.concealedKong()


    def __str__(self):
        return 'Player[%d]' % self.seatWind


    def __repr__(self):
        return self.__str__()