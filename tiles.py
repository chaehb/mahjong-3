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
        self.setType = setType


    def toTileIndexArray(self):
        '''
        Convert a TileSet to tile index array
        '''
        tiArray = []
        if self.setType == TileSet.CHOW:
            for i in range(3):
                tiArray.append(i + self.index)
        elif self.setType == TileSet.PUNG:
            for i in range(3):
                tiArray.append(self.index)
        elif self.setType == TileSet.KONG:
            for i in range(4):
                tiArray.append(self.index)
        elif self.setType == TileSet.PAIR:
            for i in range(2):
                tiArray.append(self.index)

        return tiArray


    def __eq__(self, ats):
        return ats.__class__.__name__ == 'TileSet' and \
               self.index == ats.index and \
               self.setType == ats.setType


    def __hash__(self):
        return self.index * 4 + self.setType


    def __lt__(self, ats):
        if self.index != ats.index:
            return self.index < ats.index
        else:
            return self.setType < ats.setType


    def __str__(self):
        return TileSet.TYPE_NAMES[self.setType] + '(' + str(Tiles(self.toTileIndexArray())) + ')'


    def __repr__(self):
        return self.__str__()


class Tiles:

    NUM = 38
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
            if tile in Tiles.OTHER_NAMES:
                self.tileArray[Tiles.OTHER_NAMES.index(tile) + 3 * 9] += 1
            else:
                self.tileArray[3 * Tiles.SUIT_NAMES.index(tile[1]) + int(tile[0]) - 1] += 1
        elif tile.__class__.__name__ == 'TileSet':
            for t in tile.toTileIndexArray():
                self.add(t)


    def decompose(self):
        def _decompose(tileArray, tdSet, tsArray):
            print tileArray
            print tdSet
            print tsArray
            a = raw_input('print to continue')
            found = False
            for i in range(Tiles.NUM):
                if tileArray[i] >= 2: # pair
                    nta = [] + tileArray
                    tsa = [] + tsArray
                    nta[i] -= 2
                    tsArray.append(TileSet(i, TileSet.PAIR))
                    found = True
                    _decompose(nta, tdSet, tsa)

                if tileArray[i] >= 3: # pung
                    nta = [] + tileArray
                    tsa = [] + tsArray
                    nta[i] -= 3
                    tsArray.append(TileSet(i, TileSet.PUNG))
                    found = True
                    _decompose(nta, tdSet, tsa)

                # don't need to consider kong when decomposing

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
                        tsArray.append(TileSet(i * 9 + j, TileSet.CHOW))
                        found = True
                        _decompose(nta, tdSet, tsa)

            if not found:
                tdSet.add(TileDecompostion(tsArray, Tiles(tileArray)))


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
            h += self.rest.tileArray[i] * i

        return h


    def __str__(self):
        return str(self.sets) + ' + ' + str(self.rest)


    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    ts = Tiles()
    ts.add(TileSet(0, TileSet.CHOW))
    ts.add(TileSet(1, TileSet.CHOW))
    ts.add(TileSet(10, TileSet.PUNG))
    ts.add(TileSet(12, TileSet.PUNG))
    ts.add(TileSet(22, TileSet.PAIR))

    tdSet = ts.decompose()
    for td in tdSet:
        print td
