# -*- coding: utf-8 -*-

import random
from sets import Set


class TileSet:
    '''
    A TileSet is a set that should be CHOW, PUNG, KONG or PAIR
    '''
    CHOW = 0
    PUNG = 1
    KONG = 2
    PAIR = 3

    TYPE_NAMES = ['Chow', 'Pung', 'Kong', 'Pair']

    def __init__(self, index, setType):
        self.index = index
        self.type = setType


    def toTileIndexArray(self):
        '''
        Convert a TileSet to tile index array
        '''
        tiArray = []
        if self.type == TileSet.CHOW:
            for i in range(3):
                tiArray.append(i + self.index)
        elif self.type == TileSet.PUNG:
            for i in range(3):
                tiArray.append(self.index)
        elif self.type == TileSet.KONG:
            for i in range(4):
                tiArray.append(self.index)
        elif self.type == TileSet.PAIR:
            for i in range(2):
                tiArray.append(self.index)

        return tiArray


    def __eq__(self, ats):
        return ats.__class__.__name__ == 'TileSet' and \
               self.index == ats.index and \
               self.type == ats.type


    def __hash__(self):
        return self.index * 4 + self.type


    def __lt__(self, ats):
        if self.index != ats.index:
            return self.index < ats.index
        else:
            return self.type < ats.type


    def __str__(self):
        return TileSet.TYPE_NAMES[self.type] + '(' + str(Tiles(self.toTileIndexArray())) + ')'


    def __repr__(self):
        return self.__str__()



class Tiles:

    NUM = 34
    SUIT_NAMES = ['s', 'm', 'p']
    OTHER_NAMES = ['E', 'S', 'W', 'N', 'P', 'F', 'C']

    '''
    Tiles class represents a collection of tiles
    '''

    def __init__(self, tileArray = None):
        self.tileArray = [0] * Tiles.NUM
        if tileArray:
            for t in tileArray:
                self.add(t)


    def add(self, tile):
        '''
        Add new tile into this collection. 
        Tile can be:
        1. an int value which represents the index of tile
        2. a string represents the short-hand notation
        3. a tileset
        '''
        if type(tile) == int:
            self.tileArray[tile] += 1
        elif type(tile) == str:
            self.tileArray[str2Tile(tile)] += 1
        elif tile.__class__.__name__ == 'TileSet':
            for t in tile.toTileIndexArray():
                self.add(t)


    def decompose(self, onlyWin = False):
        '''
        decompose the tiles collection to any possible tile set combinations.
        '''
        def _decompose(tileArray, tdSet, tsArray):
            found = False
            for i in range(3):
                for j in range(7):
                    if tileArray[i * 9 + j    ] > 0 and \
                       tileArray[i * 9 + j + 1] > 0 and \
                       tileArray[i * 9 + j + 2] > 0:
                        nta = [] + tileArray
                        tsa = [] + tsArray
                        nta[i * 9 + j    ] -= 1
                        nta[i * 9 + j + 1] -= 1
                        nta[i * 9 + j + 2] -= 1
                        tsa.append(TileSet(i * 9 + j, TileSet.CHOW))
                        found = True
                        _decompose(nta, tdSet, tsa)

            for i in range(Tiles.NUM):
                if tileArray[i] >= 3: # pung
                    nta = [] + tileArray
                    tsa = [] + tsArray
                    nta[i] -= 3
                    tsa.append(TileSet(i, TileSet.PUNG))
                    found = True
                    _decompose(nta, tdSet, tsa)

                if tileArray[i] >= 2: # pair
                    nta = [] + tileArray
                    tsa = [] + tsArray
                    nta[i] -= 2
                    tsa.append(TileSet(i, TileSet.PAIR))
                    found = True
                    _decompose(nta, tdSet, tsa)

                # don't need to consider kong when decomposing

            if not found:
                ts = Tiles()
                if onlyWin:
                    win = True
                    for i in range(Tiles.NUM):
                        if tileArray[i] != 0:
                            win = False
                            break
                    if win:
                        tdSet.add(TileDecompostion(tsArray, ts))
                else:
                    ts.tileArray = tileArray
                    tdSet.add(TileDecompostion(tsArray, ts))


        tdSet = Set()
        _decompose(self.tileArray, tdSet, [])
        return tdSet


    @staticmethod
    def generateShuffledTilePool():
        '''
        Generate a new tile pool and then shuffle it.
        '''
        tiles = []
        for i in range(Tiles.NUM):
            for j in range(4):
                tiles.append(i)

        random.shuffle(tiles)
        return tiles


    def __eq__(self, ats):
        return self.tileArray == ats.tileArray


    def __getitem__(self, i):
        if type(i) == int:
            return self.tileArray[i]
        elif type(i) == str:
            return self.tileArray[str2Tile(i)]


    def __setitem__(self, i, value):
        if type(i) == int:
            self.tileArray[i] = value
        elif type(i) == str:
            self.tileArray[str2Tile(i)] = value


    def __str__(self):
        '''
        Convert this collection of tiles to short-hand notation
        '''
        s = ''
        for suit in range(3):
            add = False
            for index in range(9):
                for i in range(self.tileArray[suit * 9 + index]):
                    s += str(index + 1)
                    add = True

            if add:
                s += Tiles.SUIT_NAMES[suit]

        for index in range(len(Tiles.OTHER_NAMES)):
            for i in range(self.tileArray[index + 3 * 9]):
                s += Tiles.OTHER_NAMES[index]

        return s


    def __repr__(self):
        return self.__str__()


class TileDecompostion:

    def __init__(self, sets = [], rest = Tiles()):
        self.sets = sets
        self.sets.sort()
        self.rest = rest


    def addTileSet(self, ts):
        self.sets.append(ts)
        self.sets.sort()

    def addRest(self, t):
        self.rest.add(t)


    def __eq__(self, atd):
        return self.sets == atd.sets and self.rest == atd.rest


    def __hash__(self):
        h = 0
        for s in self.sets:
            h += s.__hash__()

        for i in range(Tiles.NUM):
            h += self.rest[i] * i

        return h


    def __str__(self):
        restStr = str(self.rest)
        if restStr == '':
            return str(self.sets)
        else:
            return str(self.sets) + ' + ' +  restStr


    def __repr__(self):
        return self.__str__()


def str2Tile(tile):
    '''
    Convert tile short-hand notation to tile index
    '''
    if tile in Tiles.OTHER_NAMES:
        return Tiles.OTHER_NAMES.index(tile) + 3 * 9
    else:
        return 3 * Tiles.SUIT_NAMES.index(tile[1]) + int(tile[0]) - 1


def tile2Str(tile):
    '''
    Convert tile index to short-hand notation
    '''
    if tile < 3 * 9:
        suit = tile / 9
        index = tile % 9
        return str(index + 1) + Tiles.SUIT_NAMES[suit]
    else:
        return Tiles.OTHER_NAMES[tile - 3 * 9]
