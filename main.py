# -*- coding: utf-8 -*-

from mahjong import *
from tiles import *
from rules import *

DEBUG = True

def logger(action):
    if action['from']:
        print action['from'],

    print action['name'],

    if action['to']:
        print action['to'],

    if action['tile'] != None:
        action['tile'] = tile2Str(action['tile'])
        print action['tile'],

    if action['from']:
        print '=>', action['from'].tiles,

    print 


# game = Mahjong()
# if DEBUG:
#     game.actionListeners.append(logger)

# game.run()


ts = Tiles()

ts.add(TileSet(str2Tile('1s'), TileSet.CHOW))
ts.add(TileSet(str2Tile('7s'), TileSet.CHOW))
ts.add(TileSet(str2Tile('5p'), TileSet.CHOW))
ts.add(TileSet(str2Tile('3s'), TileSet.PUNG))
ts.add(TileSet(str2Tile('1s'), TileSet.PAIR))

j = Judger()
game = Mahjong()
game.newAction(name = 'Draw', tile = 0)

print 'Judging:', ts
score, wps = j.judge(ts.decompose(True), game)
print 'Score:', score
for wp in wps:
    print wp