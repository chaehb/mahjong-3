# -*- coding: utf-8 -*-

from mahjong import *
from tiles import *
from rules import *
import random
from pprint import *
from collections import *
from sets import Set
import itertools

ALL_COMB = itertools.combinations_with_replacement


if __name__ == '__main__':
    CHOW_COUNT = [1,2,3,3,3,3,3,2,1]

    data = {}

    for tileArray in ALL_COMB(range(5), 9):
        ts = Tiles()
        ts.tileArray = list(tileArray) + [0] * 26

        tdSet = ts.decompose()

        prop = {}


        for td in tdSet:
            for ts in td.sets:
                if ts.type == TileSet.SINGLE:
                    indexArray = ts.toTileIndexArray()
                    if indexArray[0] not in prop:
                        prop[indexArray[0]] = 0.0

                    if indexArray[0] < 3 * 9:
                        prop[indexArray[0]] += (4.0 / 136) ** 2 * CHOW_COUNT[indexArray[0] % 9]
                    else:
                        prop[indexArray[0]] += (4.0 / 136) ** 2

                elif ts.type == TileSet.M_CHOW:
                    indexArray = ts.toTileIndexArray()
                    if indexArray[0] not in prop:
                        prop[indexArray[0]] = 0.0
                    if indexArray[1] not in prop:
                        prop[indexArray[1]] = 0.0

                    prop[indexArray[0]] += 4.0 / 136
                    prop[indexArray[1]] += 4.0 / 136

                elif ts.type == TileSet.L_CHOW or ts.type == TileSet.R_CHOW:
                    indexArray = ts.toTileIndexArray()
                    if indexArray[0] not in prop:
                        prop[indexArray[0]] = 0.0
                    if indexArray[1] not in prop:
                        prop[indexArray[1]] = 0.0

                    prop[indexArray[0]] += 4.0 / 136 * 2
                    prop[indexArray[1]] += 4.0 / 136 * 2

                elif ts.type == TileSet.PAIR:
                    indexArray = ts.toTileIndexArray()
                    if indexArray[0] not in prop:
                        prop[indexArray[0]] = 0.0

                    prop[indexArray[0]] += 2.0 / 136

        propList = [(tile2Str(k), v) for k, v in prop.iteritems()]
        propList.sort(key = lambda x: x[1])
        
        data[tuple(tileArray)] = propList

    f = open('chow.py', 'w')
    f.write('CHOW_PROP = ' + str(data))
    f.close()



